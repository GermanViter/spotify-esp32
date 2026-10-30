from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

bearer_key = os.getenv("SPOTIFY_BEARER_KEY")
refresh_token = os.getenv("AQC_TOKEN")
aqa = os.getenv("REFRESH_TOKEN")
code = os.getenv("CODE")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
access_token = os.getenv("ACCESS_TOKEN")

def get_access_token():
    """Get a fresh access token using the refresh token."""
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": aqa,
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"]

def get_currently_playing():
    token = get_access_token()
    resp = requests.get(
        "https://api.spotify.com/v1/me/player/currently_playing",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code == 204:  # nothing playing
        return None
    resp.raise_for_status()
    return resp.json()

res = get_currently_playing()

print(json.dumps(res, indent=2))
