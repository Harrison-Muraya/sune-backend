"""
Sune TV - Sample Data Generator
Creates sample categories and streams for testing

Run with: python manage.py shell < create_sample_data.py
"""

from streams.models import Category, Stream

print("Creating sample data for Sune TV...")

# Create Categories
categories_data = [
    {"name": "Movies", "description": "Feature films and cinema", "order": 1},
    {"name": "Series", "description": "TV series and shows", "order": 2},
    {"name": "Documentary", "description": "Documentary films and series", "order": 3},
    {"name": "Live TV", "description": "Live streaming channels", "order": 4},
    {"name": "Sports", "description": "Sports events and highlights", "order": 5},
]

categories = {}
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data["name"],
        defaults=cat_data
    )
    categories[cat_data["name"]] = category
    if created:
        print(f"✓ Created category: {category.name}")
    else:
        print(f"○ Category already exists: {category.name}")

# Sample video URLs (using publicly available test videos)
sample_videos = {
    "big_buck_bunny": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "elephants_dream": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "for_bigger_blazes": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "for_bigger_escape": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "for_bigger_fun": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "for_bigger_joyrides": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "sintel": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    "tears_of_steel": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
}

# Create Sample Streams
streams_data = [
    {
        "title": "Big Buck Bunny",
        "description": "A large and lovable rabbit deals with three tiny bullies, led by a flying squirrel, who are determined to squelch his happiness.",
        "category": "Movies",
        "thumbnail": "https://peach.blender.org/wp-content/uploads/title_anouncement.jpg?x11217",
        "banner": "https://peach.blender.org/wp-content/uploads/poster_rodents_small.jpg?x11217",
        "url": sample_videos["big_buck_bunny"],
        "duration": "9m 56s",
        "release_year": 2008,
        "rating": 8.5,
        "quality": "HD",
        "is_featured": True,
    },
    {
        "title": "Sintel",
        "description": "A wandering warrior finds an unlikely friend in the form of a young dragon. The two develop a bond that is tested as they search for the dragon's kin.",
        "category": "Movies",
        "thumbnail": "https://durian.blender.org/wp-content/uploads/2010/06/sintel_trailer_iphone_08.jpg",
        "url": sample_videos["sintel"],
        "duration": "14m 48s",
        "release_year": 2010,
        "rating": 9.0,
        "quality": "HD",
        "is_featured": True,
    },
    {
        "title": "Tears of Steel",
        "description": "In an apocalyptic future, a group of scientists and warriors must protect the last bastion of humanity.",
        "category": "Movies",
        "thumbnail": "https://mango.blender.org/wp-content/uploads/2012/09/03_thom_celia.jpg",
        "url": sample_videos["tears_of_steel"],
        "duration": "12m 14s",
        "release_year": 2012,
        "rating": 7.8,
        "quality": "FHD",
        "is_featured": False,
    },
    {
        "title": "Elephants Dream",
        "description": "The story of two strange characters exploring a capricious and seemingly infinite machine.",
        "category": "Documentary",
        "thumbnail": "https://orange.blender.org/wp-content/themes/orange/images/media/svn_tree.jpg",
        "url": sample_videos["elephants_dream"],
        "duration": "10m 54s",
        "release_year": 2006,
        "rating": 7.2,
        "quality": "HD",
    },
    {
        "title": "For Bigger Blazes",
        "description": "Experience the thrill of adventure with stunning visuals.",
        "category": "Series",
        "thumbnail": "https://via.placeholder.com/300x200?text=For+Bigger+Blazes",
        "url": sample_videos["for_bigger_blazes"],
        "duration": "15s",
        "rating": 8.0,
        "quality": "HD",
    },
    {
        "title": "For Bigger Escapes",
        "description": "Journey through breathtaking landscapes.",
        "category": "Series",
        "thumbnail": "https://via.placeholder.com/300x200?text=For+Bigger+Escapes",
        "url": sample_videos["for_bigger_escape"],
        "duration": "15s",
        "rating": 7.5,
        "quality": "HD",
    },
    {
        "title": "For Bigger Fun",
        "description": "Entertainment for the whole family.",
        "category": "Series",
        "thumbnail": "https://via.placeholder.com/300x200?text=For+Bigger+Fun",
        "url": sample_videos["for_bigger_fun"],
        "duration": "60s",
        "rating": 8.2,
        "quality": "FHD",
    },
    {
        "title": "For Bigger Joyrides",
        "description": "Thrilling adventures await in this exciting series.",
        "category": "Sports",
        "thumbnail": "https://via.placeholder.com/300x200?text=For+Bigger+Joyrides",
        "url": sample_videos["for_bigger_joyrides"],
        "duration": "15s",
        "rating": 7.9,
        "quality": "HD",
    },
]

for stream_data in streams_data:
    category_name = stream_data.pop("category")
    stream_data["category"] = categories[category_name]
    
    stream, created = Stream.objects.get_or_create(
        title=stream_data["title"],
        defaults=stream_data
    )
    
    if created:
        print(f"✓ Created stream: {stream.title} ({stream.category.name})")
    else:
        print(f"○ Stream already exists: {stream.title}")

print("\n" + "="*50)
print("Sample data creation complete!")
print("="*50)
print(f"Categories: {Category.objects.count()}")
print(f"Streams: {Stream.objects.count()}")
print("\nYou can now:")
print("1. Access admin: http://localhost:8000/admin/")
print("2. View API: http://localhost:8000/api/streams/")
print("3. View docs: http://localhost:8000/swagger/")
