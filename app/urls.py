from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index1'),
        url(r'^index/$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^myacct/$', views.myacct, name='myacct'),
        url(r'^register/$', views.register, name='register'),
        url(r'^index/(?P<item_id>[0-9]+?)/$', views.detail, name='about'),
        url(r'^suggestions/$', views.suggestions, name='suggestions'),
        url(r'^suggestions/(?P<item_id>[0-9]+?)/$', views.suggestionsdet, name='suggestionsdet'),
        url(r'^newitem/$', views.newitem, name='newitem'),
        url(r'^searchitem/$', views.searchitem, name='searchitem'),
    ]
