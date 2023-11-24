import os
from dotenv import load_dotenv
import base64
from requests import post, get
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
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_playlist_by_id(token, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_songs_from_playlist(json_playlist):
    songs = {}
    counter = 1
    for song in json_playlist["tracks"]["items"]:
        song_key = "song"+str(counter)
        song_name = song["track"]["name"]
        song_URI = song["track"]["uri"]
        artists = []
        for artist in song["track"]["artists"]:
            artists.append(artist["name"])
        songs.update(
            {
                song_key: {
                    "title": song_name,
                    "artist": artists,
                    "URI": song_URI,
                }
            }
        )
        counter+=1
    return songs

def get_difference(playlist1,playlist2):
    common_titles = set(playlist1.keys()) & set(playlist2.keys())

    for title in common_titles:
        del playlist1[title]
    
    return playlist1

token = get_token()
json_first_playlist = get_playlist_by_id(token,"0tG8lWSuqMaZhJ1HkUyhCo")
json_second_playlist = get_playlist_by_id(token,"0CtD0CLuF8cXpLAN1H07jO")
first_playlist_songs = get_songs_from_playlist(json_first_playlist)
second_playlist_songs = get_songs_from_playlist(json_second_playlist)

different_songs = get_difference(first_playlist_songs,second_playlist_songs)
print(different_songs)
# f = open("demofile3.txt", "w")
# f.write(json.dumps(json_results,indent=4))
# f.close()

