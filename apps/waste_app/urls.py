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
    url(r'^login$', views.login),
    # url(r'^zero_waste$', views.zero_waste),
    url(r'^getcsrf/$', views.get_csrf),
    url(r'^delete/(?P<trash_id>\d+)$',views.deltrash),
    url(r'^', include(router.urls)),
]