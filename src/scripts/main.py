import os
from dotenv import load_dotenv
import base64
from requests import post,get
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def get_playlist_by_id(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url,headers=headers)
    json_result = json.loads(result.content)
    return json_result

token = get_token()
json_results = get_playlist_by_id(token,"46Vvp6M1HPCbNg1W9kcCRZ")
f = open("demofile3.txt", "w")
f.write(str(json.dumps(json_results,indent=4)))
f.close()