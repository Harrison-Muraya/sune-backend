"""
Sune TV - API Views
Handles HTTP requests and returns JSON responses
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Category, Stream, WatchHistory
from .serializers import (
    CategorySerializer,
    StreamListSerializer,
    StreamDetailSerializer,
    StreamCreateSerializer,
    WatchHistorySerializer,
    StreamsByCategorySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model
    
    list: Get all active categories
    retrieve: Get a specific category by ID
    create: Create a new category (admin only)
    update: Update a category (admin only)
    delete: Delete a category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    @action(detail=True, methods=['get'])
    def streams(self, request, slug=None):
        """
        Get all streams in a specific category
        URL: /api/categories/{slug}/streams/
        """
        category = self.get_object()
        streams = Stream.objects.filter(category=category, is_active=True)
        serializer = StreamListSerializer(streams, many=True)
        return Response(serializer.data)


class StreamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Stream model
    
    Main endpoints matching Android app requirements:
    - GET /api/streams/ - List all streams
    - GET /api/stream/{id}/ - Get stream details
    - POST /api/streams/ - Create new stream (admin)
    """
    queryset = Stream.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'quality', 'is_featured', 'is_live']
    search_fields = ['title', 'description', 'cast', 'director']
    ordering_fields = ['created_at', 'view_count', 'rating', 'title']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail"""
        if self.action == 'list':
            return StreamListSerializer
        elif self.action == 'create':
            return StreamCreateSerializer
        return StreamDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        Get stream by ID and increment view count
        URL: GET /api/stream/{id}/
        """
        instance = self.get_object()
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        Get featured streams for hero banner
        URL: /api/streams/featured/
        """
        streams = Stream.objects.filter(is_featured=True, is_active=True)[:5]
        serializer = StreamListSerializer(streams, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """
        Get streams grouped by category (matches Android app format)
        URL: /api/streams/by_category/
        
        Returns:
        [
            {
                "category": "Movies",
                "streams": [...]
            },
            {
                "category": "Series",
                "streams": [...]
            }
        ]
        """
        categories = Category.objects.filter(is_active=True)
        result = []
        
        for category in categories:
            streams = Stream.objects.filter(
                category=category,
                is_active=True
            )[:10]  # Limit to 10 streams per category
            
            if streams.exists():
                result.append({
                    'category': category.name,
                    'streams': StreamListSerializer(streams, many=True).data
                })
        
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint
        URL: /api/streams/search/?q=query
        """
        query = request.query_params.get('q', '')
        
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        streams = Stream.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(cast__icontains=query) |
            Q(director__icontains=query),
            is_active=True
        )
        
        serializer = StreamListSerializer(streams, many=True)
        return Response({
            'query': query,
            'count': streams.count(),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def live(self, request):
        """
        Get all live streams
        URL: /api/streams/live/
        """
        streams = Stream.objects.filter(is_live=True, is_active=True)
        serializer = StreamListSerializer(streams, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def trending(self, request):
        """
        Get trending streams (sorted by view count)
        URL: /api/streams/trending/
        """
        streams = Stream.objects.filter(is_active=True).order_by('-view_count')[:20]
        serializer = StreamListSerializer(streams, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def increment_view(self, request, pk=None):
        """
        Manually increment view count
        URL: POST /api/streams/{id}/increment_view/
        """
        stream = self.get_object()
        stream.increment_views()
        return Response({'view_count': stream.view_count})


class WatchHistoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Watch History
    Track what users are watching
    """
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['device_id', 'stream', 'completed']
    ordering = ['-watched_at']
    
    @action(detail=False, methods=['get'])
    def by_device(self, request):
        """
        Get watch history for a specific device
        URL: /api/watch-history/by_device/?device_id=xxx
        """
        device_id = request.query_params.get('device_id')
        
        if not device_id:
            return Response(
                {'error': 'device_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        history = WatchHistory.objects.filter(device_id=device_id)
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def track(self, request):
        """
        Track a watch event
        URL: POST /api/watch-history/track/
        Body: {
            "stream": 1,
            "device_id": "android-device-123",
            "watch_duration": 120,
            "completed": false
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)