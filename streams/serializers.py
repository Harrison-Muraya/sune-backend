from rest_framework import serializers
from .models import Category, Stream, WatchHistory

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    stream_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug',
            'description',
            'icon',
            'order',
            'stream_count',
            'created_at',
        ]
        read_only_fields = ['slug', 'created_at']
    
    def get_stream_count(self, obj):
        """Get count of active streams in this category"""
        return obj.streams.filter(is_active=True).count()


class StreamListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for stream lists (thumbnails, basic info)
    Used in HomeScreen carousels
    """
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Stream
        fields = [
            'id',
            'title',
            'thumbnail',
            'url',
            'category',
            'duration',
            'rating',
            'is_live',
        ]


class StreamDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for stream details
    Used in DetailsScreen
    """
    category = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    
    class Meta:
        model = Stream
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'thumbnail',
            'banner',
            'url',
            'category',
            'category_id',
            'duration',
            'release_year',
            'rating',
            'director',
            'cast',
            'language',
            'quality',
            'is_featured',
            'is_live',
            'view_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at']


class StreamCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new streams
    """
    class Meta:
        model = Stream
        fields = [
            'title',
            'description',
            'thumbnail',
            'banner',
            'url',
            'category',
            'duration',
            'release_year',
            'rating',
            'director',
            'cast',
            'language',
            'quality',
            'is_featured',
            'is_live',
        ]
    
    def validate_url(self, value):
        """Validate that URL is accessible (basic check)"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value
    
    def validate_rating(self, value):
        """Validate rating is between 0 and 10"""
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError("Rating must be between 0 and 10")
        return value


class WatchHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for watch history tracking
    """
    stream_title = serializers.CharField(source='stream.title', read_only=True)
    stream_thumbnail = serializers.URLField(source='stream.thumbnail', read_only=True)
    
    class Meta:
        model = WatchHistory
        fields = [
            'id',
            'stream',
            'stream_title',
            'stream_thumbnail',
            'device_id',
            'watched_at',
            'watch_duration',
            'completed',
        ]
        read_only_fields = ['watched_at']


class StreamsByCategorySerializer(serializers.Serializer):
    """
    Custom serializer for grouped streams by category
    Matches the Android app's StreamCategory model
    """
    category = serializers.CharField()
    streams = StreamListSerializer(many=True)