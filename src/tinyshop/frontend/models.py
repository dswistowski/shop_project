from collections import defaultdict
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms

class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    
    parent = models.ForeignKey('Category', null=True, blank=True)
    
    def is_leaf(self):
        return not bool(self.category_set.all())
    
    def parents(self):
        if self.parent:
            yield self.parent
            for parent in self.parent.parents():
                yield parent
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = 'title',
    
class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    
    category = models.ForeignKey(Category)
    
    def get_custom_fields(self):
        '''
        Returns list of custom fields with an value object, ordered by name
        '''
        fields = defaultdict(lambda: [])
        # group for speed up db searches
        for field in list(self.category.customfield_set.all()):
            fields[field.get_field_model()].append(field)
        data = []
        # get data from db
        for model, custom_fields in fields.iteritems():
            fields = dict((f.id, f) for f in custom_fields)
            for value in model.objects.filter(custom_field__in=custom_fields, product=self):
                data.append((fields.get(value.custom_field_id), value))
                
        # order by name
        return sorted(data, key=lambda data: data[0].name)
      
    def set_custom_field(self, custom_field, value):
        '''
        Set custom field of model, there is not test for case when product do not have value of
        selected custom_field. Testing this will take databese query, this is tested on form level
        If you force to set wrong custom_field data will be not shown from the get_custom_field.
        '''
        model = custom_field.get_field_model()
        custom_value, created = model.objects.get_or_create(custom_field=custom_field, product=self, defaults={'value': value})
        if not created:
            custom_value.value = value
            custom_value.save()
    
    def get_custom_field(self, custom_field):
        model = custom_field.get_field_model()
        return model.objects.get(custom_field=custom_field, product=self)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = 'title',

# custom fields part

class CustomField(models.Model):
    '''
    Definition of custiom fields, object of this model is 
    connected with category. Objects added to the category 
    are using this custom fields
    '''
    TYPE_INTEGER, TYPE_BOOL, TYPE_TEXT = range(3)
    TYPES = (
        (TYPE_INTEGER, _('integer')),
        (TYPE_BOOL, _('bool')),
        (TYPE_TEXT, _('text'))
    )
    category = models.ForeignKey('Category')
    name = models.CharField(max_length=250)
    type = models.IntegerField(choices=TYPES)
    
    def get_field_class(self):
        '''
        Returns field class, used to generate form
        '''
        return TYPE2FIELD_CLASS.get(self.type)(label=self.name)

    def get_field_model(self):
        '''
        Returns field model class, used to prepare queryset
        '''
        return TYPE2FIELD_MODEL.get(self.type)
        
    def __unicode__(self):
        return u'%s - %s' % (self.name, self.category)
 
class CustomFieldValueBase(models.Model):
    '''
    Common part of models which are storing value of
    custom fields, for every type of custom field there is
    a different model.
    Value models must have a field value which stores 
    the value of fields in selected type
    '''
    custom_field = models.ForeignKey(CustomField, related_name="%(app_label)s_%(class)s_related")
    product = models.ForeignKey(Product)
    
    class Meta:
        unique_together = ('custom_field', 'product')
        abstract = True
        
class IntegerValue(CustomFieldValueBase):
    value = models.IntegerField()
    
    def __unicode__(self):
        v = unicode(self.value)
        # and here is a joke
        return ' '.join(list((v[::-1][x:x + 3][::-1] for x in range(0, len(v), 3)))[::-1])
    
class BoolValue(CustomFieldValueBase):
    value = models.BooleanField()
    
    def __unicode__(self):
        if self.value:
            return unicode(_('Yes'))
        else:
            return unicode(_('No'))
    
class TextValue(CustomFieldValueBase):
    value = models.TextField()
    
    def __unicode__(self):
        return self.value

# definition classes and models of types 
# TYPE2FIELD_CLASS - is a dictionary which maps type of 
#    custom field to form field class, or to delegate of this class
# TYPE2FIELD_MODELS - maps type to  model class for values of this type
TYPE2FIELD_CLASS = {
    CustomField.TYPE_INTEGER: forms.IntegerField,
    CustomField.TYPE_BOOL: lambda * args, **kwargs: forms.BooleanField(*args, required=False, **kwargs),
    CustomField.TYPE_TEXT: lambda * args, **kwargs: forms.CharField(*args, widget=forms.Textarea, **kwargs)
}

TYPE2FIELD_MODEL = {
    CustomField.TYPE_INTEGER: IntegerValue,
    CustomField.TYPE_BOOL: BoolValue,
    CustomField.TYPE_TEXT: TextValue,
}
