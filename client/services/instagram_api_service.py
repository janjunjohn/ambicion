import requests
import environ
import json

# Set Environment Variables
env = environ.Env()
environ.Env.read_env()

_GRAPH_API_ID = env('GRAPH_API_ID')
_GRAPH_API_ACCESS_TOKEN = env('GRAPH_API_ACCESS_TOKEN')
_BASE_URL = f"https://graph.facebook.com/v19.0/{_GRAPH_API_ID}/media"


class InstagramAPIService:
    @classmethod
    def get_recent_posts(self, post_num: int) -> dict[str, str]:
        parameters = {
            "fields":"media_url,like_count,permalink",
            "limit":post_num,
            "access_token":_GRAPH_API_ACCESS_TOKEN
        }
        response = requests.get(_BASE_URL, params=parameters)
        data = response.json()['data']
        return data
