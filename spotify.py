#!./venv/bin/python

import json
import os
import env
import sys
import time

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

_cached_token = None
_token_expires_at = 0

def get_access_token():
    global _cached_token, _token_expires_at
    now = time.time()
    if _cached_token and now < _token_expires_at:
        return _cached_token

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
        _cached_token = resp.json()["access_token"]
        _token_expires_at = now + 3500  # ponytail: 100s safety margin
        return _cached_token
    finally:
        resp.close()

def get_currently_playing():
    token = get_access_token()
    resp = requests.get(
        "https://api.spotify.com/v1/me/player/currently_playing",
        headers={"Authorization": f"Bearer {token}"},
    )
    try:
        if resp.status_code == 401:  # Token might be stale
            global _cached_token
            _cached_token = None
            token = get_access_token()
            resp = requests.get(
                "https://api.spotify.com/v1/me/player/currently_playing",
                headers={"Authorization": f"Bearer {token}"},
            )

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
