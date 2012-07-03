"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils.translation import gettext_lazy as _
from django import forms
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from tinyshop.frontend.models import Category, CustomField, IntegerValue, \
    TextValue, BoolValue, Product
from tinyshop.frontend.forms import ProductFormFactory

class BaseTestCase(TestCase):
    def setUp(self):
        self.r1 = Category.objects.create(title="Cars", slug="cars")
        self.r2 = Category.objects.create(title="Trucks", slug="trucks")
        self.r3 = Category.objects.create(title="Super cars", slug="super-cars", parent=self.r1)
        self.r4 = Category.objects.create(title="Super super cars", slug="super-super-cars", parent=self.r3)
        self.c1 = CustomField.objects.create(id=1, category=self.r4, name="Model", type=CustomField.TYPE_TEXT)
        self.c2 = CustomField.objects.create(id=2, category=self.r4, name="Type", type=CustomField.TYPE_TEXT)
        self.c3 = CustomField.objects.create(id=3, category=self.r4, name="Engine size", type=CustomField.TYPE_INTEGER)
        self.c4 = CustomField.objects.create(id=4, category=self.r4, name="Used", type=CustomField.TYPE_BOOL)
        self.c5 = CustomField.objects.create(id=5, category=self.r2, name="Description", type=CustomField.TYPE_TEXT)
        
    def tearDown(self):
        for x in [self.r1, self.r2, self.r3, self.r4]:
            x.delete()


class ModelsTestCase(BaseTestCase):
    
    def testCustomFieldModels(self):
        self.assertEqual(self.c1.get_field_model(), TextValue)
        self.assertEqual(self.c3.get_field_model(), IntegerValue)
        self.assertEqual(self.c4.get_field_model(), BoolValue)
        
    def testCustomFieldClass(self):
        self.assertIsInstance(self.c1.get_field_class(), forms.CharField)
        self.assertIsInstance(self.c3.get_field_class(), forms.IntegerField)
        self.assertIsInstance(self.c4.get_field_class(), forms.BooleanField)
        
    def testNewProduct(self):
        Form = ProductFormFactory(self.r4)
        # test if form has all the fields and field has good classes
        r4cf = [self.c1, self.c2, self.c3, self.c4]
        key_maker = lambda c: 'custom_field_%d' % c.id
        for c in r4cf:
            self.assertEqual(Form().fields[key_maker(c)].__class__, c.get_field_class().__class__)
        # c5 shoud not be in this form
        self.assertNotIn(key_maker(self.c5), Form().fields)
        
        # lets create proper object
        data = {
            'custom_field_1': 'Renault',
            'custom_field_2': 'Clio',
            'custom_field_3': '123',
            'custom_field_4': True,
            'title': 'Renault Clio',
            'slug': 'clio',
            'category': self.r4.id
        }
            
            
        form = Form(data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        
        # custom field corrent values in alphabetic order
        self.assertEqual(
            [(f.name, v.value) for f, v in instance.get_custom_fields()],
            [(u'Engine size', 123), (u'Model', u'Renault'), (u'Type', u'Clio'), (u'Used', True)])
        
        self.assertEqual(TextValue.objects.all().count(), 2) # there should be 2 text values model and engine
        
        # save the same object 2 time:
        form = Form(data)
        self.assertFalse(form.is_valid())
        data['slug'] = 'clio-2'
        form = Form(data)
        self.assertTrue(form.is_valid())
        
        
    def testNewProductBadData(self):
        data = {
            'custom_field_1': 'Renault',
            'custom_field_2': 'Clio',
            'custom_field_4': True,
            'title': 'Renault Clio',
            'slug': 'clio',
            'category': self.r4.id
        }
        Form = ProductFormFactory(self.r4)
        form = Form(data)
        # no field_3
        self.assertFalse(form.is_valid())
        # bad format of field 3
        data['custom_field_3'] = '19a' 
        form = Form(data)
        self.assertFalse(form.is_valid())
        
    def testProduct(self):
        product = Product.objects.create(title='Clio', category=self.r4, slug='clio')
        # there is no values
        self.assertEqual(TextValue.objects.all().count(), 0)
        product.set_custom_field(self.c1, 'Clio')
        # created
        self.assertEqual(TextValue.objects.all().count(), 1)
        product.set_custom_field(self.c1, 'Clio II')
        # edited
        self.assertEqual(TextValue.objects.all().count(), 1)
        product.set_custom_field(self.c2, 'super clio')
        # created
        self.assertEqual(TextValue.objects.all().count(), 2)
        product.set_custom_field(self.c3, '23')
        product.set_custom_field(self.c4, False)
        
        # irrelevant, should be not showed in get_custom_fields
        product.set_custom_field(self.c5, 'sadd')
        
        self.assertEqual(
            [(f.name, v.value) for f, v in product.get_custom_fields()],
            [(u'Engine size', 23), (u'Model', u'Clio II'), (u'Type', u'super clio'), (u'Used', False)])
    
    def testIsLeaf(self):
        self.assertTrue(self.r4.is_leaf())
        self.assertFalse(self.r4.parent.is_leaf())
    
    def testCategoryParents(self):
        self.assertEqual(list(self.r4.parents()), [self.r3, self.r1])
        self.assertEqual(list(self.r3.parents()), [self.r1])
        self.assertEqual(list(self.r1.parents()), [])
    
    def testCanBeUnicoded(self):
        unicode(self.r1)
        unicode(self.c1)
        product = Product.objects.create(title='Clio', category=self.r4, slug='clio')
        self.assertEqual(unicode(product), u'Clio')
        product.delete()
        
    def testDisplayValues(self):
        product = Product.objects.create(title='Clio', category=self.r4, slug='clio')
        product.set_custom_field(self.c1, 'Clio')
        cv = product.get_custom_field(self.c1)
        self.assertEqual(unicode(cv), 'Clio')
        
        product.set_custom_field(self.c3, '1200')
        cv = product.get_custom_field(self.c3)
        self.assertEqual(unicode(cv), u'1 200')
        
        product.set_custom_field(self.c4, True)
        cv = product.get_custom_field(self.c4)
        self.assertEqual(unicode(cv), _('Yes'))
        
        product.set_custom_field(self.c4, False)
        cv = product.get_custom_field(self.c4)
        self.assertEqual(unicode(cv), _('No'))
        
        product.delete()

class ViewsTestCase(BaseTestCase):

    def testIndexPage(self):
        c = Client()
        response = c.get(reverse('category_root'))
        self.assertTemplateUsed(response, 'frontend/category_list.html')
        
    def testCategoryList(self):
        c = Client()
        response = c.get(reverse('category_list', kwargs={'parent': self.r1.slug}))
        self.assertTemplateUsed(response, 'frontend/category_list.html')

    def testProductDetail(self):
        product = Product.objects.create(title='Clio', category=self.r4, slug='clio')
        product.set_custom_field(self.c1, 'Clio Field')
        product.set_custom_field(self.c2, 'Super Clio')
        product.set_custom_field(self.c3, '1200')
        product.set_custom_field(self.c4, True)
        
        c = Client()
        response = c.get(reverse('product_detail', kwargs={'slug': product.slug}))
        self.assertContains(response, 'Clio Field')
        self.assertContains(response, 'Super Clio')
        self.assertContains(response, '1 200')
        self.assertContains(response, unicode(_('Yes')))
        product.delete()
        
    def testNewProductView(self):
        c = Client()
        response = c.get(reverse('product_create', kwargs={'parent': self.r4.slug}))
        self.assertContains(response, 'Engine size')
        self.assertTemplateUsed(response, 'frontend/product_form.html')
        data = {  
            'custom_field_1': 'Renault',
            'custom_field_2': 'Clio',
            'custom_field_3': '1200',
            'custom_field_4': True,
            'title': 'Renault Clio',
            'slug': 'clio',
            'category': self.r4.id
        }
        response = c.post(
            reverse('product_create', kwargs={'parent': self.r4.slug}),
            data,
        )
        self.assertRedirects(response, reverse('category_list', kwargs={'parent': self.r4.slug}))
        product = Product.objects.get(slug='clio')
        self.assertEqual(product.title, 'Renault Clio')
        self.assertEqual(product.category, self.r4)
        self.assertEqual(unicode(product.get_custom_field(self.c1)), 'Renault')
        product.delete()
    
    def testWrongCustomFieldData(self):
        c = Client()
        data = {  
            'custom_field_1': 'Renault',
            'custom_field_2': 'Clio',
            'custom_field_3': 'HERE TEXT IS NOT ALLOWED',
            'custom_field_4': True,
            'title': 'Renault Clio',
            'slug': 'clio',
            'category': self.r4.id
        }
        response = c.post(
            reverse('product_create', kwargs={'parent': self.r4.slug}),
            data,
        )
        self.assertTemplateUsed(response, 'frontend/product_form.html')
