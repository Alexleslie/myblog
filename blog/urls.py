from django.conf.urls import url,include
from . import views
from django.conf.urls import handler404, handler500
app_name = 'blog'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^search/$', views.search, name='search'),
    url(r'^outside/$', views.outside, name='outside'),
    url(r'^message/$', views.message, name='message'),
    url(r'^register/$', views.register, name='register'),
    url(r'^users/', include('django.contrib.auth.urls')),
]
