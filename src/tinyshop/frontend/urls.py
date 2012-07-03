from django.conf.urls.defaults import patterns, url

from tinyshop.frontend.views import CategoryView, ProductCreateView, ProductView


urlpatterns = patterns('tinyshop.frontend.views',
    url(r'^$', CategoryView.as_view(), {'parent': None}, name='category_root'),
    url(r'^category/(?P<parent>[^/]+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^product/(?P<parent>[^/]+)/new/$', ProductCreateView.as_view(), name='product_create'),
    url(r'^product/(?P<slug>[^/]+)/$', ProductView.as_view(), name='product_detail'),
)
