from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuideAPIViewSet

router = DefaultRouter()
router.register('guides', GuideAPIViewSet, basename='guides')

urlpatterns = [
    path('', include(router.urls))
]