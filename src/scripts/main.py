from authorization.spotify_auth import get_token
from spotify_api.playlist_data import get_playlist_by_id, get_songs_from_playlist, get_differences
import eel
import os

eel.init(os.path.dirname(__file__) + str("/web"))
eel.start("index.html", port = 8080)


@eel.expose                         # Expose this function to Javascript
def say_hello_py(x):
    print('Hello from %s' % x)

say_hello_py('Python World!')
eel.say_hello_js('Python World!')   # Call a Javascript function

eel.start('hello.html')             # Start (this blocks and enters loop)




# token = get_token()
# json_first_playlist = get_playlist_by_id(token,"46Vvp6M1HPCbNg1W9kcCRZ")
# json_second_playlist = get_playlist_by_id(token,"0CtD0CLuF8cXpLAN1H07jO")
# first_playlist_songs = get_songs_from_playlist(json_first_playlist)
# second_playlist_songs = get_songs_from_playlist(json_second_playlist)

# different_songs = get_differences(first_playlist_songs,second_playlist_songs)
# print(different_songs.keys())



#https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows
