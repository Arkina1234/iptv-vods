import json
import requests

# Get categories
categories_response = requests.get("https://stirr.com/api/videos/categories/?type=is_video")
categories_data = categories_response.json()

# Get first category
category_id = categories_data['categories'][0]['category_id']
category_name = categories_data['categories'][0]['category_name']

# Get videos for the category
videos_response = requests.get(f"https://stirr.com/api/videos/list/?categories={category_id}")
videos_data = videos_response.json()

# Extract video information
videos = []
category_videos = videos_data['videos']['category_videos'][str(category_id)]

for video in category_videos:
    video_info = {
        "name": video.get('title'),
        "category": category_name,
        "info": {
            "poster": video.get('portrait_thumbs', {}).get('original'),
            "plot": video.get('description'),
            "rating": video.get('rating'),
            "year": video.get('year'),
            "duration": video.get('duration_in_seconds')
        },
        "video": video.get('live')
    }
    videos.append(video_info)

# Save to output file
with open('/api/stirr.json', 'w', encoding='utf-8') as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)

print("Data saved to stirr.json")
