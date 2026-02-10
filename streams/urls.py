from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, StreamViewSet, WatchHistoryViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'streams', StreamViewSet, basename='stream')
router.register(r'watch-history', WatchHistoryViewSet, basename='watch-history')

urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
    
    # Custom endpoint matching Android app requirements exactly
    # GET /api/streams - Already handled by router
    # GET /api/stream/{id} - Need to add this specific format
]

# Add custom URL for /api/stream/{id} to match Android app expectation
from .views import StreamViewSet

urlpatterns += [
    path('stream/<int:pk>/', StreamViewSet.as_view({'get': 'retrieve'}), name='stream-detail-alt'),
]






