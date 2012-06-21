from zope import interface
from zope import component
from zope.annotation.interfaces import IAttributeAnnotatable, IAnnotations

ANNOTATION_KEY = 'QA_ANN'

class IAnnotationManager(interface.Interface):
    """
    Annotation manager...
    read annotation from any plone (annotable) content
    """
    def read():
        """return ANNOTATION_KEY content """
        
    def write(data):
        """write input dict to ANNOTATION_KEY"""

class AnnotationManager():
    interface.implements(IAnnotationManager)
    component.adapts(IAttributeAnnotatable)
    
    def __init__(self , context):
        self.context = context
    
    def read(self):
        annotations = IAnnotations(self.context)
        return annotations[ANNOTATION_KEY]
    
    def write(self , data):
        annotations = IAnnotations(self.context)
        new_dict = {}
        for k in data.keys():
            new_dict[k] = data[k]
        annotations[ANNOTATION_KEY] = new_dict
