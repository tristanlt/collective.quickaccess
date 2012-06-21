from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from zope import schema
from zope import interface

from plone.autoform.form import AutoExtensibleForm
from z3c.form import form , button , error
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError
from plone.z3cform import layout
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations

from collective.quickaccess.annotationmgr import IAnnotationManager

class bar(ViewletBase):
    render = ViewPageTemplateFile('quickaccess.pt')
    def update(self):
            an = IAnnotationManager(self.context)
            self.activate=True
            try:
                content = an.read()
            except:
                content={'qablock':False,'qatext':'','qalinks':''}
            self.qaLinksList=[]
            self.qablock=content['qablock']
            self.qatext=content['qatext']
            for linkline in content['qalinks'].split("\n"):
                link=linkline.split(';')[0]
                url=linkline.split(';')[1]
                self.qaLinksList.append({'link':link,'url':url})

class IQuickAccessManage(interface.Interface):
    """metadata form"""
    qablock = schema.Bool(title=u"Herit", description=u"Herit QuickAccess in this section (and childrens)",default=True)
    qatext = schema.TextLine(title=u"Text", description=u"Text to introduce quickaccess bar",
                              required=False)
    qalinks = schema.Text(title=u"Links", description=u"Please enter one link per line, separate link and URL by semicolon (;)",
                              required=False)

class QaManage(AutoExtensibleForm , form.Form):
    """A form to manage QuickAccess bar content"""
    schema = IQuickAccessManage
    # desactive ignoreContext et on surcharge la methode getContent
    # afin de pre-remplir le formulaire avec les valeurs existantes
    ignoreContext = False

    def getContent(self):
        an = IAnnotationManager(self.context)
        try:
            content = an.read()
        except:
            content={'qablock':'False','qatext':'','qalinks':''}
        return content

    @button.buttonAndHandler(u"Save")
    def save(self,action):
        data , errors = self.extractData()
        if errors:
            return
        an = IAnnotationManager(self.context)
        try:
            an.write(data)
        except ValueError:
            IStatusMessage(self.context).add('Error in data')

class QaManageForm(layout.FormWrapper):
    label = u"QuickAccess Manager"
    form = QaManage
