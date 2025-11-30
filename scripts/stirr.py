import requests
import json

def get_stirr_data():
    # Get video categories
    videos_categories_url = "https://stirr.com/api/videos/categories/?type=is_video"
    series_categories_url = "https://stirr.com/api/series/categories/?type=is_series"
    
    # Get categories for both videos and series
    videos_categories_response = requests.get(videos_categories_url)
    series_categories_response = requests.get(series_categories_url)
    
    videos_categories_data = videos_categories_response.json()
    series_categories_data = series_categories_response.json()
    
    all_data = []
    
    # Process video categories
    if 'categories' in videos_categories_data:
        for category in videos_categories_data['categories']:
            category_id = category.get('category_id')
            category_name = category.get('category_name')
            
            # Get videos for this category
            videos_list_url = f"https://stirr.com/api/videos/list/?categories={category_id}"
            videos_response = requests.get(videos_list_url)
            videos_data = videos_response.json()
            
            # Process videos
            if ('videos' in videos_data and 
                'category_videos' in videos_data['videos'] and 
                str(category_id) in videos_data['videos']['category_videos']):
                
                for video in videos_data['videos']['category_videos'][str(category_id)]:
                    video_data = {
                        "name": video.get('title', ''),
                        "category": category_name,
                        "info": {
                            "poster": video.get('portrait_thumbs', {}).get('original') if video.get('portrait_thumbs') else None,
                            "bg": video.get('thumbs', {}).get('original') if video.get('thumbs') else None,
                            "plot": video.get('description'),
                            "rating": video.get('rating'),
                            "year": video.get('year'),
                            "duration": video.get('duration_in_seconds')
                        },
                        "video": video.get('live', '')
                    }
                    all_data.append(video_data)
    
    # Process series categories
    if 'categories' in series_categories_data:
        for category in series_categories_data['categories']:
            category_id = category.get('category_id')
            category_name = category.get('category_name')
            
            # Get series for this category
            series_list_url = f"https://stirr.com/api/series/list/?categories={category_id}"
            series_response = requests.get(series_list_url)
            series_data = series_response.json()
            
            # Process series
            if ('series' in series_data and 
                'category_series' in series_data['series'] and 
                str(category_id) in series_data['series']['category_series']):
                
                for series in series_data['series']['category_series'][str(category_id)]:
                    series_id = series.get('series_id')
                    series_seasons = []
                    
                    # Get seasons for this series
                    season_list_url = f"https://stirr.com/api/season/list/{series_id}"
                    season_response = requests.get(season_list_url)
                    season_data = season_response.json()
                    
                    if season_data.get('data') and 'seasons' in season_data['data']:
                        for season in season_data['data']['seasons']:
                            season_id = season.get('season_id')
                            season_sequence = season.get('sequence')
                            episodes_list = []
                            
                            # Get episodes for this season
                            season_data_url = f"https://stirr.com/api/season/data?series_id={series_id}&season_id={season_id}"
                            episode_response = requests.get(season_data_url)
                            episode_data = episode_response.json()
                            
                            if episode_data.get('data'):
                                for episode in episode_data['data']:
                                    episode_data_item = {
                                        "episode": episode.get('sequence'),
                                        "name": episode.get('title', ''),
                                        "category": category_name,
                                        "info": {
                                            "poster": episode.get('thumbs', {}).get('original') if episode.get('thumbs') else None,
                                            "plot": episode.get('description'),
                                            "rating": episode.get('rating'),
                                            "year": episode.get('year'),
                                            "duration": episode.get('duration_in_seconds')
                                        },
                                        "video": episode.get('live', '')
                                    }
                                    episodes_list.append(episode_data_item)
                            
                            season_data_item = {
                                "season": season_sequence,
                                "episodes": episodes_list
                            }
                            series_seasons.append(season_data_item)
                    
                    series_data_item = {
                        "name": series.get('series_name', ''),
                        "category": category_name,
                        "info": {
                            "poster": series.get('portrait_thumbs', {}).get('original') if series.get('portrait_thumbs') else None,
                            "bg": series.get('thumbs', {}).get('original') if series.get('thumbs') else None,
                            "plot": series.get('series_description'),
                            "rating": series.get('rating'),
                            "year": series.get('year')
                        },
                        "seasons": series_seasons
                    }
                    all_data.append(series_data_item)
    
    return all_data

def save_to_file(data, filename="api/stirr.json"):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    try:
        print("Fetching data from STIRR...")
        data = get_stirr_data()
        
        print(f"Retrieved {len(data)} items")
        
        # Save to file
        save_to_file(data)
        print("Data saved to api/stirr.json")
        
        # Also print JSON to console
        print(json.dumps(data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
