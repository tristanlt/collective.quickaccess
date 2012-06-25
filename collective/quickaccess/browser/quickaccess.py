from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

from zope import schema
from zope import interface

from plone.autoform.form import AutoExtensibleForm
from z3c.form import form , button , error
from z3c.form.interfaces import ActionExecutionError, WidgetActionExecutionError
from plone.z3cform import layout
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from Acquisition import aq_inner, aq_parent

from collective.quickaccess.annotationmgr import IAnnotationManager


class bar(ViewletBase):
    render = ViewPageTemplateFile('quickaccess.pt')
    def update(self):
            self.activate=True
            try:
                an = IAnnotationManager(self.context)
            except:
                self.activate=False
            if self.activate:
                content=self.readQA(self.context)
                if content['qatext'] == None:
                    content['qatext'] = ''
                if content['qalinks'] == None:
                    content['qalinks'] = ''
                if content['qalinks'] != '':
                    self.activate=True
                    self.qaLinksList=[]
                    self.qaherit=content['qaherit']
                    self.qatext=content['qatext']
                    for linkline in content['qalinks'].split("\n"):
                        link=linkline.split(';')[0]
                        url=linkline.split(';')[1]
                        self.qaLinksList.append({'link':link,'url':url})
                else:
                    self.activate=False
            else:
                self.activate=False

    def readQA(self, object2read):
            an = IAnnotationManager(object2read)
            isAnnotation=True
            try:
                content = an.read()
            except:
                isAnnotation=False
                
            if isAnnotation:
                # CAS d'arrive au repertoire racine
                if object2read.id =='Plone' and content['qalinks'] != '':
                    return content
                if content['qaherit'] == True:
                    return self.readQA(aq_inner(object2read).aq_parent)
                else:
                    return content
            else:
                if object2read.id =='Plone':
                    content={'qaherit':False,'qatext':'','qalinks':''}
                    return content
                return self.readQA(aq_inner(object2read).aq_parent)

class IQuickAccessManage(interface.Interface):
    """metadata form"""
    qaherit = schema.Bool(title=u"Herit", description=u"Herit QuickAccess in this section (and childrens)",default=True)
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
            content={'qaherit':'False','qatext':'','qalinks':''}
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
