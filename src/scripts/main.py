import PySimpleGUI as sg
from authorization.spotify_auth import get_token
from spotify_api.playlist_data import get_playlist_by_id, get_songs_from_playlist, get_differences





token = get_token()
json_first_playlist = get_playlist_by_id(token,"46Vvp6M1HPCbNg1W9kcCRZ")
json_second_playlist = get_playlist_by_id(token,"0CtD0CLuF8cXpLAN1H07jO")
first_playlist_songs = get_songs_from_playlist(json_first_playlist)
second_playlist_songs = get_songs_from_playlist(json_second_playlist)

different_songs = get_differences(first_playlist_songs,second_playlist_songs)
print(different_songs.keys())



# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]



# # Create the window
# window = sg.Window("Git-Tunes", layout)

# # Create an event loop
# while True:
#     event, values = window.read()
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break

# window.close()

# f = open("demofile3.txt", "w")
# f.write(json.dumps(json_results,indent=4))
# f.close()

