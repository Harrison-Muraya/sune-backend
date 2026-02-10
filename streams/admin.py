"""
Sune TV - Django Admin Configuration
Provides a web interface to manage streams, categories, and watch history
"""

from django.contrib import admin
from .models import Category, Stream, WatchHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model
    """
    list_display = ['name', 'slug', 'order', 'stream_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    
    def stream_count(self, obj):
        """Display count of streams in category"""
        return obj.streams.filter(is_active=True).count()
    stream_count.short_description = 'Active Streams'


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    """
    Admin interface for Stream model
    """
    list_display = [
        'title',
        'category',
        'quality',
        'duration',
        'rating',
        'view_count',
        'is_featured',
        'is_live',
        'is_active',
        'created_at'
    ]
    list_filter = [
        'category',
        'quality',
        'is_featured',
        'is_live',
        'is_active',
        'created_at'
    ]
    search_fields = ['title', 'description', 'cast', 'director']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Media', {
            'fields': ('thumbnail', 'banner', 'url', 'quality')
        }),
        ('Metadata', {
            'fields': ('duration', 'release_year', 'rating', 'director', 'cast', 'language')
        }),
        ('Status', {
            'fields': ('is_featured', 'is_live', 'is_active')
        }),
        ('Analytics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_featured', 'remove_featured', 'activate', 'deactivate']
    
    def make_featured(self, request, queryset):
        """Mark selected streams as featured"""
        count = queryset.update(is_featured=True)
        self.message_user(request, f'{count} stream(s) marked as featured.')
    make_featured.short_description = 'Mark as featured'
    
    def remove_featured(self, request, queryset):
        """Remove featured status from selected streams"""
        count = queryset.update(is_featured=False)
        self.message_user(request, f'{count} stream(s) removed from featured.')
    remove_featured.short_description = 'Remove from featured'
    
    def activate(self, request, queryset):
        """Activate selected streams"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} stream(s) activated.')
    activate.short_description = 'Activate selected streams'
    
    def deactivate(self, request, queryset):
        """Deactivate selected streams"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} stream(s) deactivated.')
    deactivate.short_description = 'Deactivate selected streams'


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Watch History
    """
    list_display = [
        'stream',
        'device_id',
        'watch_duration_formatted',
        'completed',
        'watched_at'
    ]
    list_filter = ['completed', 'watched_at']
    search_fields = ['stream__title', 'device_id']
    readonly_fields = ['watched_at']
    date_hierarchy = 'watched_at'
    
    def watch_duration_formatted(self, obj):
        """Format watch duration in minutes"""
        minutes = obj.watch_duration // 60
        seconds = obj.watch_duration % 60
        return f"{minutes}m {seconds}s"
    watch_duration_formatted.short_description = 'Duration Watched'