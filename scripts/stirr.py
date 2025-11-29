import json
import requests

# Get categories
categories_response = requests.get("https://stirr.com/api/videos/categories/?type=is_video")
categories_data = categories_response.json()

videos_list = []

# Loop through all categories
for category in categories_data.get('categories', []):
    category_id = category.get('category_id')
    category_name = category.get('category_name')
    
    # Get videos for this category
    videos_response = requests.get(f"https://stirr.com/api/videos/list/?categories={category_id}")
    videos_data = videos_response.json()
    
    # Get category videos
    category_videos = videos_data.get('videos', {}).get('category_videos', {}).get(str(category_id), [])
    
    # Loop through videos in this category
    for video in category_videos:
        title = video.get('title')
        description = video.get('description')
        rating = video.get('rating')
        video_url = video.get('live')
        portrait_thumbs = video.get('portrait_thumbs', {}).get('original') if video.get('portrait_thumbs') else None
        year = video.get('year')
        duration = video.get('duration_in_seconds')
        
        # Create video object
        video_obj = {
            "name": title,
            "category": category_name,
            "info": {
                "poster": portrait_thumbs,
                "plot": description,
                "rating": rating,
                "year": year,
                "duration": duration
            },
            "video": video_url
        }
        
        videos_list.append(video_obj)

# Save to output file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(videos_list, f, indent=2, ensure_ascii=False)

print(f"Saved {len(videos_list)} videos to output.json")
