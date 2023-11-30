from authorization.spotify_auth import get_new_token, get_auth_code, get_refresh_token, get_authorization_URL
from spotify_api.playlist_data import (
    get_playlist_by_id,
    get_songs_from_playlist,
    get_differences,
    add_to_playlist,
)

import os
import json
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QApplication,
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton,
    QLineEdit,
    QCheckBox


)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6 import QtCore
from PyQt6.QtCore import Qt, QUrl, QEventLoop
import sys




class SongApp(QWidget):
    def __init__(self):
        super().__init__()

        # Sample dictionary of songs
        self.spotify_auth_url = get_authorization_URL()
        print(self.spotify_auth_url)
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
        self.token = ""
        if self.get_spotify_token():
            self.initUI()

    def get_spotify_token(self):

        auth_window = AuthWindow(self.spotify_auth_url, self)
        auth_window.setGeometry(100, 100, 800, 600)
        auth_window.show()

        # Wait for the authentication window to be closed
        auth_window.wait_for_close()

        # Extract the redirect URL from the authentication window
        redirect_url = auth_window.result

        # Handle the redirect URL as needed (e.g., extract the token)
        if redirect_url:
            print("Redirect URL:", redirect_url)
            # Implement logic to extract token from the redirect_url
            # For example, you might parse the URL to get the token.

            # Simulate successful token retrieval
            return True
        else:
            print("Authentication failed")
            # Handle the case where authentication failed
            return False

    def initUI(self):
        layout = QVBoxLayout()

        # Create list widget to display songs
        self.song_list_widget = QListWidget(self)
        self.populate_song_list()
        layout.addWidget(self.song_list_widget)

        # Create submit button
        submit_button = QPushButton("Submit", self)
        submit_button.clicked.connect(self.on_submit)
        layout.addWidget(submit_button)

        # Set the layout
        self.setLayout(layout)

        # Set window properties
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle("Select Songs")

    def populate_song_list(self):
        # Populate the list widget with songs from the dictionary
        for song in self.songs.items():
            # Create a custom QListWidgetItem
            item = QListWidgetItem(self.song_list_widget)
            self.song_list_widget.addItem(item)

            # Create a QCheckBox
            title = song[1]["title"]
            artists = ','.join(song[1]["artist"])
            checkbox = QCheckBox(f"{title} - {artists}")
            checkbox.setChecked(False)  # Initially unchecked
            item.setSizeHint(checkbox.sizeHint())  # Set item size based on the checkbox

            # Set the custom widget as the item widget
            self.song_list_widget.setItemWidget(item, checkbox)

    def on_submit(self):
        # Modify the dictionary based on selected songs
        for i in range(self.song_list_widget.count()):
            item = self.song_list_widget.item(i)
            checkbox = self.song_list_widget.itemWidget(item)
            song_key = list(self.songs.keys())[i]
            self.songs[song_key]["picked"] = checkbox.isChecked()

        # Print or use the modified dictionary
        print("Updated Songs:", self.songs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SongApp()
    form.show()
    sys.exit(app.exec())


#This will check if a refresh token exists, and if it doesn't or there's an error, it'll get a new code.
token = get_refresh_token()
print("hellooooo")
json_first_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0tG8lWSuqMaZhJ1HkUyhCo?si=8bf6f26f84d6426a")
json_second_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0CtD0CLuF8cXpLAN1H07jO?si=323512ab01b44220")
first_playlist_songs = get_songs_from_playlist(json_first_playlist)
second_playlist_songs = get_songs_from_playlist(json_second_playlist)

different_songs = get_differences(first_playlist_songs,second_playlist_songs)

print(different_songs)

test = json.dumps(different_songs)
different_songs["song1"]["picked"] = True

add_to_playlist(token,"0CtD0CLuF8cXpLAN1H07jO",different_songs)


# https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows


# class MyForm(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         layout = QGridLayout()

#         self.playlist_to_copy = QLineEdit()
#         self.playlist_to_copy.setPlaceholderText("Playlist to copy from")
#         self.playlist_to_be_copied = QLineEdit()
#         self.playlist_to_be_copied.setPlaceholderText("Playlist to copy to")

#         layout.addWidget(QLabel("Playlist #1"),0,0)
#         layout.addWidget(self.playlist_to_copy, 1, 0)
#         layout.addWidget(QLabel("Playlist #2"),2,0)
#         layout.addWidget(self.playlist_to_be_copied, 3, 0)

#         submit_button = QPushButton('Submit', self)
#         submit_button.clicked.connect(self.on_submit)
#         layout.addWidget(submit_button,4,0)

#         self.setLayout(layout)

#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('Submit Text Boxes')

#     def on_submit(self):
#         playlist_to_copy_URL = self.playlist_to_copy.text()
#         playlist_to_be_copied_URL = self.playlist_to_be_copied.text()

#         json_first_playlist = get_playlist_by_id(token,playlist_to_copy_URL)
#         json_second_playlist = get_playlist_by_id(token,playlist_to_be_copied_URL)

#         if


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     form = MyForm()
#     form.show()
#     sys.exit(app.exec())