import requests
import json
import time
from airflow.models import Variable
from airflow.hooks.base_hook import BaseHook


def get_access_token():

    token_url = 'https://accounts.spotify.com/api/token'
    # Load secrets from Airflow connection
    spotify_conn = BaseHook.get_connection('spotify_api')
    client_id = spotify_conn.extra_dejson.get('client_id')
    client_secret = spotify_conn.extra_dejson.get('client_secret')

    # Load from Airflow Variables
    try:
        token_info = json.loads(Variable.get("spotify_token_info"))
    except KeyError:
        raise Exception("Airflow Variable 'spotify_token_info' not found. Set it up in the UI.")
    
    now = int(time.time())
    if token_info['expires_in'] - now < 60:
        print("Refreshing Spotify token...")
        response = requests.post(token_url, data={
            "grant_type": "refresh_token",
            "refresh_token": token_info['refresh_token'],
            "client_id": client_id,
            "client_secret": client_secret
        })

        if response.status_code != 200:
            raise Exception("Failed to refresh token.")

        new_token = response.json()
        token_info.update({
            "access_token": new_token["access_token"],
            "expires_in": now + new_token["expires_in"],
            "refresh_token": new_token.get("refresh_token", token_info["refresh_token"])
        })

        # Save updated token info back to Airflow Variable
        Variable.set("spotify_token_info", json.dumps(token_info))

    return token_info["access_token"]
