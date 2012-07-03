# Create your views here.
from django.views.generic.list import ListView, MultipleObjectMixin
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.core.urlresolvers import reverse

from tinyshop.frontend.forms import ProductFormFactory
from tinyshop.frontend.models import Category, Product


class CategoryListBaseMixIn(object):
    def get_context_data(self, **kwargs):
        context = super(CategoryListBaseMixIn, self).get_context_data(**kwargs)
        context.update(category=self.get_current_category())
        return context
    
    def get_current_category(self):
        if not hasattr(self, '_current_category'):
            parent = self.kwargs.get('parent')
            if parent:
                self._current_category = get_object_or_404(Category, slug=parent)
            else:
                self._current_category = None
        return self._current_category

class CategoryListMixIn(CategoryListBaseMixIn, MultipleObjectMixin):
    pass

class CategoryViewMixIn(CategoryListBaseMixIn, SingleObjectMixin):
    pass

class CategoryView(ListView, CategoryListMixIn):
    def get_queryset(self):
        parent = self.get_current_category()
        if parent:
            return parent.category_set.all()
        else:
            return Category.objects.filter(parent=None)

class ProductView(CategoryViewMixIn, DetailView):
    queryset = Product.objects.all()
    
    def get_current_category(self):
        return self.get_object().category
    
class ProductCreateView(CategoryViewMixIn, CreateView):
    model = Product
    
    def get_form_class(self):
        return ProductFormFactory(self.get_current_category())
    
    def get_success_url(self):
        return reverse('category_list', kwargs={'parent': self.kwargs.get('parent')})
    
    def get_initial(self):
        return {'category': self.get_current_category()}

