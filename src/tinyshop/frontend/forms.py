from django import forms
from django.forms.models import ModelFormMetaclass

from tinyshop.frontend.models import Product, Category


class ProductFormMetaBase(ModelFormMetaclass):
    '''
    Metaclass used to generate form fields for custom_field in product form
    '''
    def __new__(cls, name, bases, attrs):
        if 'custom_fields' in attrs:
            custom_fields = {}
            for custom_field in attrs.get('custom_fields'):
                key = 'custom_field_%d' % custom_field.id
                attrs[key] = custom_field.get_field_class()
                custom_fields[key] = custom_field
            attrs['custom_fields'] = custom_fields
        
        return ModelFormMetaclass.__new__(cls, name, bases, attrs)

class ProductFormBase(forms.ModelForm):
    '''
    Class to overide metaclass of modelform, and save values of custom fields
    '''
    __metaclass__ = ProductFormMetaBase
    
    def save(self, *args, **kwargs):
        instance = super(ProductFormBase, self).save(*args, **kwargs)
        for key, custom_field in self.custom_fields.iteritems():
            instance.set_custom_field(custom_field, self.cleaned_data.get(key))
        return instance

def ProductFormFactory(category):
    '''
    Factory of product form for selected category. Form will have and field for custom fields used in
    this category
    '''
    custom_fields_ = list(category.customfield_set.all())
    
    class ProductForm(ProductFormBase):
        custom_fields = custom_fields_ 
        category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.HiddenInput)
        
        class Meta:
            model = Product
            
    return ProductForm
