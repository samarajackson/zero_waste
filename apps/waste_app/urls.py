from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.register),
    url(r'^dashboard$', views.success),
    #actually log into the application by calling this url
    url(r'^user_login$', views.login),
    #load the login page
    url(r'^login$', views.load_login),
    url(r'^logout$', views.logout),
    url(r'^take_out_trash$', views.take_out_trash),
    url(r'^zero_waste$',views.zero_waste),
    url(r'^trash$',views.trash),
    url(r'^delete/(?P<trash_id>\d+)$',views.deltrash)
]