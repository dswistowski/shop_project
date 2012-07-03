from django.contrib import admin
from tinyshop.frontend.models import Category, CustomField

class CustomFieldInline(admin.StackedInline):
    model = CustomField

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ("title",)}
    list_display = 'title', 'parent'
    inlines = CustomFieldInline,
    ordering = '-parent',

admin.site.register(Category, CategoryAdmin)
