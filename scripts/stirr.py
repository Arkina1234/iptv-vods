import requests
import json

def get_stirr_data():
    # Get video categories or series categories
    video_categories_url = "https://stirr.com/api/videos/categories/?type=is_video"
    series_categories_url = "https://stirr.com/api/series/categories/?type=is_series"
    
    # Choose which type to process (video or series)
    process_videos = True  # Set to False to process series instead
    
    if process_videos:
        # Get video categories
        response = requests.get(video_categories_url)
        categories_data = response.json()
        
        data = []
        
        # Process each category
        for category in categories_data.get('categories', []):
            category_id = category.get('category_id')
            category_name = category.get('category_name')
            
            # Get videos for this category
            videos_url = f"https://stirr.com/api/videos/list/?categories={category_id}"
            videos_response = requests.get(videos_url)
            videos_data = videos_response.json()
            
            # Process videos in this category
            category_videos = videos_data.get('videos', {}).get('category_videos', {}).get(str(category_id), [])
            
            for video in category_videos[:5]:  # Limit to first 5 videos per category
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
                data.append(video_info)
                
    else:
        # Get series categories
        response = requests.get(series_categories_url)
        categories_data = response.json()
        
        data = []
        
        # Process each category
        for category in categories_data.get('categories', [])[:3]:  # Limit to first 3 categories
            category_id = category.get('category_id')
            category_name = category.get('category_name')
            
            # Get series for this category
            series_url = f"https://stirr.com/api/series/list/?categories={category_id}"
            series_response = requests.get(series_url)
            series_data = series_response.json()
            
            # Process series in this category
            category_series = series_data.get('series', {}).get('category_series', {}).get(str(category_id), [])
            
            for series in category_series[:2]:  # Limit to first 2 series per category
                series_id = series.get('series_id')
                series_info = {
                    "name": series.get('series_name'),
                    "category": category_name,
                    "info": {
                        "poster": series.get('portrait_thumbs', {}).get('original'),
                        "plot": series.get('series_description'),
                        "rating": series.get('rating'),
                        "year": series.get('year')
                    },
                    "seasons": []
                }
                
                # Get seasons for this series
                seasons_url = f"https://stirr.com/api/season/list/{series_id}"
                seasons_response = requests.get(seasons_url)
                seasons_data = seasons_response.json()
                
                # Process seasons
                for season in seasons_data.get('data', {}).get('seasons', [])[:2]:  # Limit to first 2 seasons
                    season_id = season.get('season_id')
                    season_number = season.get('sequence')
                    
                    season_info = {
                        "season": season_number,
                        "episodes": []
                    }
                    
                    # Get episodes for this season
                    episodes_url = f"https://stirr.com/api/season/data?series_id={series_id}&season_id={season_id}"
                    episodes_response = requests.get(episodes_url)
                    episodes_data = episodes_response.json()
                    
                    # Process episodes
                    for episode in episodes_data.get('data', [])[:3]:  # Limit to first 3 episodes
                        episode_info = {
                            "episode": episode.get('sequence'),
                            "name": episode.get('title'),
                            "category": category_name,
                            "info": {
                                "poster": episode.get('thumbs', {}).get('original'),
                                "plot": episode.get('description'),
                                "rating": episode.get('rating'),
                                "year": episode.get('year'),
                                "duration": episode.get('duration_in_seconds')
                            },
                            "video": episode.get('live')
                        }
                        season_info["episodes"].append(episode_info)
                    
                    series_info["seasons"].append(season_info)
                
                data.append(series_info)
    
    return data

def save_to_file(data, filename="api/stirr.json"):
    """Save the data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Get the data
    result_data = get_stirr_data()
    
    # Print the JSON result
    print(json.dumps(result_data, indent=2))
    
    # Save to file
    save_to_file(result_data)
    print(f"\nData saved to api/stirr.json")
