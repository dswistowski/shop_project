# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Category'
        db.create_table('frontend_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Category'], null=True, blank=True)),
        ))
        db.send_create_signal('frontend', ['Category'])

        # Adding model 'Product'
        db.create_table('frontend_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Category'])),
        ))
        db.send_create_signal('frontend', ['Product'])

        # Adding model 'CustomField'
        db.create_table('frontend_customfield', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('frontend', ['CustomField'])

        # Adding model 'IntegerValue'
        db.create_table('frontend_integervalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('custom_field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='frontend_integervalue_related', to=orm['frontend.CustomField'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Product'])),
            ('value', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('frontend', ['IntegerValue'])

        # Adding unique constraint on 'IntegerValue', fields ['custom_field', 'product']
        db.create_unique('frontend_integervalue', ['custom_field_id', 'product_id'])

        # Adding model 'BoolValue'
        db.create_table('frontend_boolvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('custom_field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='frontend_boolvalue_related', to=orm['frontend.CustomField'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Product'])),
            ('value', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('frontend', ['BoolValue'])

        # Adding unique constraint on 'BoolValue', fields ['custom_field', 'product']
        db.create_unique('frontend_boolvalue', ['custom_field_id', 'product_id'])

        # Adding model 'TextValue'
        db.create_table('frontend_textvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('custom_field', self.gf('django.db.models.fields.related.ForeignKey')(related_name='frontend_textvalue_related', to=orm['frontend.CustomField'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['frontend.Product'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('frontend', ['TextValue'])

        # Adding unique constraint on 'TextValue', fields ['custom_field', 'product']
        db.create_unique('frontend_textvalue', ['custom_field_id', 'product_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'TextValue', fields ['custom_field', 'product']
        db.delete_unique('frontend_textvalue', ['custom_field_id', 'product_id'])

        # Removing unique constraint on 'BoolValue', fields ['custom_field', 'product']
        db.delete_unique('frontend_boolvalue', ['custom_field_id', 'product_id'])

        # Removing unique constraint on 'IntegerValue', fields ['custom_field', 'product']
        db.delete_unique('frontend_integervalue', ['custom_field_id', 'product_id'])

        # Deleting model 'Category'
        db.delete_table('frontend_category')

        # Deleting model 'Product'
        db.delete_table('frontend_product')

        # Deleting model 'CustomField'
        db.delete_table('frontend_customfield')

        # Deleting model 'IntegerValue'
        db.delete_table('frontend_integervalue')

        # Deleting model 'BoolValue'
        db.delete_table('frontend_boolvalue')

        # Deleting model 'TextValue'
        db.delete_table('frontend_textvalue')


    models = {
        'frontend.boolvalue': {
            'Meta': {'unique_together': "(('custom_field', 'product'),)", 'object_name': 'BoolValue'},
            'custom_field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frontend_boolvalue_related'", 'to': "orm['frontend.CustomField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Product']"}),
            'value': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'frontend.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Category']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'frontend.customfield': {
            'Meta': {'object_name': 'CustomField'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.integervalue': {
            'Meta': {'unique_together': "(('custom_field', 'product'),)", 'object_name': 'IntegerValue'},
            'custom_field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frontend_integervalue_related'", 'to': "orm['frontend.CustomField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Product']"}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'frontend.product': {
            'Meta': {'object_name': 'Product'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'frontend.textvalue': {
            'Meta': {'unique_together': "(('custom_field', 'product'),)", 'object_name': 'TextValue'},
            'custom_field': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'frontend_textvalue_related'", 'to': "orm['frontend.CustomField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['frontend.Product']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['frontend']
