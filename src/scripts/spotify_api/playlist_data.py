from authorization.spotify_auth import get_auth_header, get_token
from requests import post, get
import json

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

def get_differences(playlist1,playlist2):
    common_titles = set(item1['title'] for item1 in playlist1.values()) & set(item2['title'] for item2 in playlist2.values())
    dict1 = {key: value for key, value in playlist1.items() if value['title'] not in common_titles}
    return dict1

def add_to_playlist(token,playlist_to_add,URI_songs_to_add):
    return