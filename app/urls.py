from django.conf.urls import url, include

from app.views import SuggestionView
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index1'),
        url(r'^index/$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^myacct/$', views.myacct, name='myacct'),
        url(r'^register/$', views.register, name='register'),
        url(r'^index/(?P<item_id>[0-9]+?)/$', views.detail, name='about'),
        url(r'^suggestions/$', views.suggestions, name='suggestions'),
        url(r'^newitem/$', views.newitem, name='newitem'),
        url(r'^searchitem/$', views.searchitem, name='searchitem'),
        url(r'^login/$', views.login_user, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^myitems/$', views.myitems, name='myitems'),
        url(r'^myitems/(?P<item_id>[0-9]+?)/$', views.detail, name='myitems'),
        url(r'^forgotpwd/$', views.forgotpwd, name='forgotpwd'),
        url(r'^checkuname/$', views.checkuname, name='checkuname'),
        url(r'^setpwd/$', views.setpwd, name='setpwd'),
        url(r'^suggestions/(?P<item_id>[0-9]+?)/$', SuggestionView.as_view())
    ]
