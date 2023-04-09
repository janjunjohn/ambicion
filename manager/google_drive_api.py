from pydrive2.auth import GoogleAuth
import yaml
import environ

# Set Environment Variables
env = environ.Env()
environ.Env.read_env()

# Write yaml file with environment variables
with open('../settings.yaml', 'w') as yf:
  yaml.dump({
    "client_config_backend": "settings",
    "client_config": {
        "client_id": env('GD_CLIENT_ID'),
        "client_secret": env('GD_CLIENT_SECRET'),
    }
  }, yf, default_flow_style=False)

# gauth = GoogleAuth()
# # Create local webserver and auto handles authentication.
# gauth.LocalWebserverAuth()