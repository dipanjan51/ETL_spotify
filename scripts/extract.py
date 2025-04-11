import pandas as pd
import requests
import datetime

from auth import get_access_token

def return_dataframe():
    print("Fetching recently played tracks from Spotify...")
    
    TOKEN = get_access_token()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    today = datetime.datetime.now()
    month_back = today - datetime.timedelta(days=30) 
    month_back_unix_timestamp = int(month_back.timestamp()) * 1000

    response = requests.get(f"https://api.spotify.com/v1/me/player/recently-played?limit=50&after={month_back_unix_timestamp}", headers = headers)

    if response.status_code != 200:
        raise Exception(f"Failed API call: {response.status_code} - {response.text}")


    data = response.json()

    if "items" not in data or len(data["items"]) == 0:
        print("No recently played tracks found in the last 30 days.")
        return pd.DataFrame()  # Return empty df
    
    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    return song_df


    