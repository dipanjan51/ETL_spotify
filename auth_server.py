import os
from flask import Flask, request, redirect
from dotenv import load_dotenv
import requests
import json

app = Flask(__name__)

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-read-recently-played"

@app.route("/")
def login():
    auth_url = (
        f"https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    code = request.args.get("code")

    token_url = "https://accounts.spotify.com/api/token"

    response = requests.post(token_url, data={
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })

    if response.status_code != 200:
        return f"Error: {response.json()}"

    token_data = response.json()

    with open("token_info.json", "w") as f:
        json.dump(token_data, f, indent=4)
    
    return "Authorization successful! Refresh token saved."

if __name__ == "__main__":
    app.run(port=8888)