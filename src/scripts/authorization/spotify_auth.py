import string
from dotenv import load_dotenv
import os
import json
import base64
from requests import post
from urllib.parse import urlencode
import random

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = "https://localhost/"

given_state = None

def get_refresh_token():
    token_url = "https://accounts.spotify.com/api/token"
    lines = []
    with open("src/assets/tokens.txt") as my_file:
        for line in my_file:
            lines.append(line)
    refresh_token = lines[0].split("=")[1].replace("\n", "")
    auth_code = lines[1].split("=")[1].replace("\n", "")
    #
    token_headers = {
        "Authorization": "Basic " + get_auth_encoded_string(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": redirect_url,
    }
    result = post(token_url, data=body, headers=token_headers)
    token_data = json.loads(result.content)
    if result.status_code == 200:
        return token_data["access_token"]
    return None

def get_authorization_code(response_url):
    response_params = dict(pair.split("=") for pair in response_url.split("&"))
    auth_code = response_params["https://localhost/?code"]
    returned_state = response_params["state"]
    if returned_state != given_state:
        print("State Error")
        exit()
    return auth_code

def get_authorization_URL():
    global given_state
    given_state = "".join(random.choice(string.ascii_letters) for i in range(16))
    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_url,
        "scope": "playlist-modify-private playlist-modify-public user-modify-playback-state",
        "state": given_state,
    }
    return "https://accounts.spotify.com/authorize?" + urlencode(auth_params)

def get_new_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    token_params = {
        "code": auth_code,
        "redirect_uri": redirect_url,
        "grant_type": "authorization_code",
    }
    token_headers = {
        "Authorization": "Basic " + get_auth_encoded_string(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    result = post(token_url, data=token_params, headers=token_headers)
    token_data = json.loads(result.content)
    if result.status_code == 200:
        refresh_token = token_data["refresh_token"]
        with open("src/assets/tokens.txt", 'r+') as file:
            file.seek(0)
            file.write(f"refresh_token={refresh_token}\n")
        return token_data["access_token"]
    else:
        print("ruh roh")
        exit()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_auth_encoded_string():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    return str(base64.b64encode(auth_bytes), "utf-8")