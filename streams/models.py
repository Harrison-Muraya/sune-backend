from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Category model for organizing streams
    Examples: Movies, Series, Documentary, Live TV
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Stream(models.Model):
    """
    Stream model representing a video/show/movie
    Contains all metadata needed by the Android app
    """
    # Basic Information
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Media Files
    thumbnail = models.URLField(max_length=500, help_text="Thumbnail image URL")
    banner = models.URLField(max_length=500, blank=True, help_text="Large banner image URL (optional)")
    url = models.URLField(max_length=500, help_text="Video stream URL (MP4, HLS, etc.)")
    
    # Categorization
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='streams'
    )
    
    # Metadata
    duration = models.CharField(max_length=50, blank=True, help_text="e.g., '2h 15m' or '45m'")
    release_year = models.IntegerField(blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, help_text="Rating out of 10")
    
    # Additional Info
    director = models.CharField(max_length=255, blank=True)
    cast = models.TextField(blank=True, help_text="Comma-separated list of actors")
    language = models.CharField(max_length=50, blank=True, default="English")
    
    # Streaming Details
    quality = models.CharField(
        max_length=20,
        choices=[
            ('SD', 'Standard Definition'),
            ('HD', 'High Definition'),
            ('FHD', 'Full HD'),
            ('4K', '4K Ultra HD'),
        ],
        default='HD'
    )
    
    # Status
    is_featured = models.BooleanField(default=False, help_text="Show on featured carousel")
    is_live = models.BooleanField(default=False, help_text="Is this a live stream?")
    is_active = models.BooleanField(default=True)
    
    # Analytics
    view_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['is_featured', '-created_at']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Use banner as thumbnail fallback if not provided
        if not self.banner and self.thumbnail:
            self.banner = self.thumbnail
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.category.name})"
    
    def increment_views(self):
        """Increment view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class WatchHistory(models.Model):
    """
    Track user watch history (optional - for future analytics)
    """
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='watch_history')
    device_id = models.CharField(max_length=255, help_text="Android device ID")
    watched_at = models.DateTimeField(auto_now_add=True)
    watch_duration = models.IntegerField(default=0, help_text="Seconds watched")
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-watched_at']
        verbose_name_plural = "Watch Histories"
    
    def __str__(self):
        return f"{self.device_id} watched {self.stream.title}"