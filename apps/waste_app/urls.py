from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from apps.waste_app import rest_views
from . import views
from django.views.generic import TemplateView

router = DefaultRouter()

router.register(r"^trashtest", rest_views.TrashViewSet)
router.register(r"^user", rest_views.UserViewSet)

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r"^$", TemplateView.as_view(template_name="index.html")),
    url(r"^monthlyleaderboard", views.monthly_leaderboard),
    url(r"^annualleaderboard", views.annual_leaderboard),
    url(r"^mydashboard", views.my_dashboard),
    url(r"^login$", views.login),
    url(r"^logout$", views.logout),
    url(r"^", include(router.urls)),
]
