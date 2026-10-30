#!./venv/bin/python

import json
import os
import env
import sys

if sys.implementation.name == "micropython":
    import urequests as requests
else:
    import requests

bearer_key = env.SPOTIFY_BEARER_KEY
refresh_token = env.REFRESH_TOKEN
code = env.CODE
client_id = env.CLIENT_ID
client_secret = env.CLIENT_SECRET
access_token = env.ACCESS_TOKEN

def get_access_token():
    body = "grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}".format(
        refresh_token, client_id, client_secret
    )
    resp = requests.post(
        "https://accounts.spotify.com/api/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        if resp.status_code != 200:
            raise OSError("token refresh failed: %d" % resp.status_code)
        return resp.json()["access_token"]
    finally:
        resp.close()

def get_currently_playing():
    token = get_access_token()
    resp = requests.get(
        "https://api.spotify.com/v1/me/player/currently_playing",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        if resp.status_code == 204:  # nothing playing
            return None
        if resp.status_code != 200:
            raise OSError("api error: %d" % resp.status_code)
        song = resp.json()

        return {
            "name": song["item"]["name"],
            "album": song["item"]["album"]["name"],
            "artist": song["item"]["artists"][0]["name"],
            "progress_ms": song["progress_ms"],
            "duration_ms": song["item"]["duration_ms"],
            "is_playing": song["is_playing"],
        }
    finally:
        resp.close()
    
if __name__ == "__main__":
    res = get_currently_playing()
    if sys.implementation.name == "micropython":
        print(res)
    else:
        print(json.dumps(res, indent=2))
