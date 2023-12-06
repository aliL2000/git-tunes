from authorization.spotify_auth import get_auth_header, get_new_token
from requests import post, get
import json
import re

def get_playlist_id(playlist_url):
    match = re.search(r"playlist/([^?]+)", playlist_url)
    playlist_id = ""
    if match:
        playlist_id = match.group(1)
    return playlist_id

def get_playlist_by_id(token, playlist_id):

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_auth_header(token)

    result = get(url, headers=headers)
    if result.status_code == 200:
        json_result = json.loads(result.content)
        return json_result
    elif result.status_code == 404:
        return {"error": "Not found Playlist"}
    else:
        return {}


def get_songs_from_playlist(json_playlist):
    songs = {}
    counter = 1
    for song in json_playlist["tracks"]["items"]:
        song_key = "song" + str(counter)
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
                    "picked": False,
                }
            }
        )
        counter += 1
    return songs


def get_differences(playlist1, playlist2):
    common_titles = set(item1["title"] for item1 in playlist1.values()) & set(
        item2["title"] for item2 in playlist2.values()
    )
    dict1 = {
        key: value
        for key, value in playlist1.items()
        if value["title"] not in common_titles
    }
    return dict1


def add_to_playlist(token, playlist_ID_to_add_to, picked_songs_dictionary):
    filtered_keys = {
        key: value
        for key, value in picked_songs_dictionary.items()
        if value["picked"] == True
    }
    URI_of_songs_to_add = []
    for song in filtered_keys.values():
        URI_of_songs_to_add.append(song["URI"])

    url = f"https://api.spotify.com/v1/playlists/{playlist_ID_to_add_to}/tracks"

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    }
    data = {"uris": URI_of_songs_to_add}
    result = post(url, headers=headers, data=json.dumps(data))
    json_result = json.loads(result.content)
    print(json_result)
    return
