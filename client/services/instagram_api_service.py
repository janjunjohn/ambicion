import requests
import environ

# Set Environment Variables
env = environ.Env()
environ.Env.read_env()

_BASE_URL = "https://graph.facebook.com/v19.0/"
_GRAPH_API_ID = env('GRAPH_API_ID')
_GRAPH_API_ACCESS_TOKEN = env('GRAPH_API_ACCESS_TOKEN')


class InstagramAPIService:
    