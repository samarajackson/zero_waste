from django.conf.urls import url
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib import admin
from django.views.generic import TemplateView

router = DefaultRouter()

router.register(r'^trashtest', views.TrashViewSet)
router.register(r'^user', views.UserViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^monthlyleaderboard', views.MonthlyLeaderboardView.as_view()),
    url(r'^annualleaderboard', views.annualLeaderboard),
    url(r'^mydashboard', views.my_dashboard),
    url(r'^userdata', views.get_user_data),
    # url(r'^create_user$', user_detail, name='user_detail'),
    # url(r'^$', views.index),
    # url(r'^create', views.register),
    # url(r'^dashboard$', views.my_dashboard),
    #actually log into the application by calling this url
    url(r'^login$', views.login),
    #load the login page
    # url(r'^login$', views.load_login),
    # url(r'^take_out_trash$', views.take_out_trash),
    url(r'^zero_waste$',views.zero_waste),
    # url(r'^trash$',views.trash),
    url(r'^delete/(?P<trash_id>\d+)$',views.deltrash),
    url(r'^', include(router.urls)),
]