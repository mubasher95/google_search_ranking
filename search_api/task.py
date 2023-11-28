import requests
from celery import shared_task

from .creds import *

@shared_task
def perform_search_task(url, keywords_list):

    base_url = "https://www.googleapis.com/customsearch/v1?"

    index_position = {}

    for query in keywords_list:

        positions = []
        search_items = []

        for start_num in range(1, 6):

            params = {
                "q":f"{query}",
                "key":gcs_api_key,
                "cx":search_engine_id,
                'start': start_num,
                "num":10
            }

            try:
                response = requests.get(base_url, params=params)
                search_items.extend(response.json().get("items",[]))

            except Exception as e:
                return {
                    "error":f"Error in Google Custom Search API request: {e}"
                }

        for i, item in enumerate(search_items, start=1):

            try:
                result_url = item.get("link", '')
                if result_url.startswith(url):
                    positions.append(i)
                    break
            except:
                pass

        index_position[query] = positions[0] if positions else None
        
    result_dict = {
        "url": url, 
        "indexing":index_position
    }

    return result_dict
