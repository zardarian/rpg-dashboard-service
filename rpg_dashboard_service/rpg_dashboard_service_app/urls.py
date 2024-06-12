from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rpg_dashboard_service_app.modules.dashboard.controllers import RpgDashboardViewSet

router = DefaultRouter()
router.register(r'dashboard', RpgDashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
