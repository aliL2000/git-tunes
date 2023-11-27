from authorization.spotify_auth import get_token, get_auth_code
from spotify_api.playlist_data import get_playlist_by_id, get_songs_from_playlist, get_differences,add_to_playlist

import os
import json


token = get_token(get_auth_code())

json_first_playlist = get_playlist_by_id(token,"46Vvp6M1HPCbNg1W9kcCRZ")
json_second_playlist = get_playlist_by_id(token,"0CtD0CLuF8cXpLAN1H07jO")
first_playlist_songs = get_songs_from_playlist(json_first_playlist)
second_playlist_songs = get_songs_from_playlist(json_second_playlist)

different_songs = get_differences(first_playlist_songs,second_playlist_songs)

test = json.dumps(different_songs)
different_songs["song1"]["picked"] = True

add_to_playlist(token,"0CtD0CLuF8cXpLAN1H07jO",different_songs)


#https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows
