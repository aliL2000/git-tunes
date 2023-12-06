from authorization.spotify_auth import get_authorization_code, get_new_token
from spotify_api.playlist_data import (
    get_playlist_by_id,
    get_songs_from_playlist,
    get_differences,
    add_to_playlist,
    get_playlist_id
)
from authorization.user_authentication import obtain_spotify_redirect
import os
import json
from PyQt6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QCheckBox,
)
import sys


class SongApp(QWidget):
    def __init__(self):
        super().__init__()

        # Sample dictionary of songs
        self.songs = {
            "song1": {
                "title": "End of Line",
                "artist": ["Daft Punk"],
                "URI": "spotify:track:09TlxralXOGX35LUutvw7I",
                "picked": False,
            },
            "song2": {
                "title": "Una Mattina",
                "artist": ["Ludovico Einaudi"],
                "URI": "spotify:track:0Dkibk70FDp6t7eOZNemNQ",
                "picked": False,
            },
            "song3": {
                "title": "TURN IT UP",
                "artist": ["Cochise"],
                "URI": "spotify:track:0uUljDsi9o1MXjReM6uLzz",
                "picked": False,
            },
            "song4": {
                "title": "Can You Hear The Music",
                "artist": ["Ludwig Göransson"],
                "URI": "spotify:track:4VnDmjYCZkyeqeb0NIKqdA",
                "picked": False,
            },
            "song5": {
                "title": "Luminary",
                "artist": ["Joel Sunny"],
                "URI": "spotify:track:66pWxtaxTV8CxcGOvivZeT",
                "picked": False,
            },
            "song6": {
                "title": "The Streak",
                "artist": ["Mychael Danna"],
                "URI": "spotify:track:0vNY5T9ovcOxqA8B6QOATk",
                "picked": False,
            },
            "song7": {
                "title": "Like a Tattoo",
                "artist": ["Sade"],
                "URI": "spotify:track:4PEGwWH4tL6H7dGl4uVSPg",
                "picked": False,
            },
            "song8": {
                "title": "King of Curses, Fire Arrow",
                "artist": ["James Liam Figueroa"],
                "URI": "spotify:track:5Mm6Nr9uzhQVOnsw0HDQqH",
                "picked": False,
            },
            "song9": {
                "title": "Cornfield Chase",
                "artist": ["Hans Zimmer"],
                "URI": "spotify:track:6pWgRkpqVfxnj3WuIcJ7WP",
                "picked": False,
            },
        }
        self.token = obtain_spotify_redirect()
        if "https://localhost/?code" in self.token:
            self.token = get_new_token(get_authorization_code(self.token))
        if self.token:
            self.initUI()
        else:
            print("There was a problem authenticating the application")
            exit()

    def initUI(self):
        layout = QGridLayout()

        # Create list widget to display songs
        self.playlist_to_copy = QLineEdit()
        self.playlist_to_copy.setPlaceholderText("Playlist to copy from")
        self.playlist_to_be_copied = QLineEdit()
        self.playlist_to_be_copied.setPlaceholderText("Playlist to copy to")

        layout.addWidget(QLabel("Playlist #1"))
        layout.addWidget(self.playlist_to_copy)
        layout.addWidget(QLabel("Playlist #2"))
        layout.addWidget(self.playlist_to_be_copied)

        submit_button = QPushButton("Submit Playlists", self)
        submit_button.clicked.connect(self.on_submit_playlists)
        layout.addWidget(submit_button)

        self.song_list_widget = QListWidget(self)
        # self.populate_song_list()
        layout.addWidget(self.song_list_widget)

        # Create submit button
        submit_button = QPushButton("Submit Songs", self)
        submit_button.clicked.connect(self.on_submit_playlist_differences)
        layout.addWidget(submit_button)

        # Set the layout
        self.setLayout(layout)

        # Set window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Select Songs")

    def on_submit_playlists(self):
        playlist_to_copy_URL = self.playlist_to_copy.text()
        playlist_to_be_copied_URL = self.playlist_to_be_copied.text()

        playlist_to_copy_ID = get_playlist_id(playlist_to_copy_URL)
        playlist_to_copy_ID = get_playlist_id(playlist_to_be_copied_URL)

        json_first_playlist = get_playlist_by_id(self.token,playlist_to_copy_ID)
        json_second_playlist = get_playlist_by_id(self.token,playlist_to_copy_ID)
        
        if "error" in json_first_playlist or "error" in json_second_playlist:
            print("Looks like we could not find the playlist you had in mind, re-try the link")
        else:
            self.songs = get_differences(get_songs_from_playlist(json_first_playlist),get_songs_from_playlist(json_second_playlist))
            self.populate_song_list()

    def populate_song_list(self):
        # Populate the list widget with songs from the dictionary
        for song in self.songs.items():
            # Create a custom QListWidgetItem
            item = QListWidgetItem(self.song_list_widget)
            self.song_list_widget.addItem(item)

            # Create a QCheckBox
            title = song[1]["title"]
            artists = ",".join(song[1]["artist"])
            checkbox = QCheckBox(f"{title} - {artists}")
            checkbox.setChecked(False)  # Initially unchecked
            item.setSizeHint(checkbox.sizeHint())  # Set item size based on the checkbox

            # Set the custom widget as the item widget
            self.song_list_widget.setItemWidget(item, checkbox)

    def on_submit_playlist_differences(self):
        # Modify the dictionary based on selected songs
        for i in range(self.song_list_widget.count()):
            item = self.song_list_widget.item(i)
            checkbox = self.song_list_widget.itemWidget(item)
            song_key = list(self.songs.keys())[i]
            self.songs[song_key]["picked"] = checkbox.isChecked()

        # Print or use the modified dictionary
        print("Updated Songs:", self.songs)
        add_to_playlist(self.token,get_playlist_id(self.playlist_to_be_copied.text),self.songs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SongApp()
    form.show()
    sys.exit(app.exec())


# This will check if a refresh token exists, and if it doesn't or there's an error, it'll get a new code.
# token = get_refresh_token()
# print("hellooooo")
# json_first_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0tG8lWSuqMaZhJ1HkUyhCo?si=8bf6f26f84d6426a")
# json_second_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0CtD0CLuF8cXpLAN1H07jO?si=323512ab01b44220")
# first_playlist_songs = get_songs_from_playlist(json_first_playlist)
# second_playlist_songs = get_songs_from_playlist(json_second_playlist)

# different_songs = get_differences(first_playlist_songs,second_playlist_songs)

# print(different_songs)

# test = json.dumps(different_songs)
# different_songs["song1"]["picked"] = True

# add_to_playlist(token,"0CtD0CLuF8cXpLAN1H07jO",different_songs)


# https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows
