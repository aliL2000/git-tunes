from authorization.spotify_auth import get_new_token, get_auth_code, get_refresh_token
from spotify_api.playlist_data import (
    get_playlist_by_id,
    get_songs_from_playlist,
    get_differences,
    add_to_playlist,
)

import os
import json
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QPushButton, QLineEdit
import sys

# This will check if a refresh token exists, and if it doesn't or there's an error, it'll get a new code.
# token = get_refresh_token()

# json_first_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0tG8lWSuqMaZhJ1HkUyhCo?si=8bf6f26f84d6426a")
# json_second_playlist = get_playlist_by_id(token,"https://open.spotify.com/playlist/0CtD0CLuF8cXpLAN1H07jO?si=323512ab01b44220")
# first_playlist_songs = get_songs_from_playlist(json_first_playlist)
# second_playlist_songs = get_songs_from_playlist(json_second_playlist)

# different_songs = get_differences(first_playlist_songs,second_playlist_songs)

# test = json.dumps(different_songs)
# different_songs["song1"]["picked"] = True

# add_to_playlist(token,"0CtD0CLuF8cXpLAN1H07jO",different_songs)


# https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows
def main():
    """PyCalc's main function."""
    # app = QApplication([])
    # window = QWidget()
    # window.setWindowTitle("PyQt App")
    # window.setGeometry(100, 100, 280, 80)
    # helloMsg = QLabel("<h1>Hello, World!</h1>", parent=window)
    # helloMsg.move(60, 15)
    # window.show()

    app = QApplication([])
    window = QWidget()
    window.setWindowTitle("QGridLayout")

    playlist_to_copy = QLineEdit()
    playlist_to_copy.setPlaceholderText("Playlist to copy from")
    playlist_to_be_copied = QLineEdit()
    playlist_to_be_copied.setPlaceholderText("Playlist to copy to")

    layout = QGridLayout()
    layout.addWidget(playlist_to_copy, 0, 0)
    layout.addWidget(QPushButton("Submit"), 0, 1)
    layout.addWidget(playlist_to_be_copied, 1, 0)
    layout.addWidget(QPushButton("Submit"), 1, 1)
    layout.addWidget(QPushButton("Button (2, 1) + 2 Columns Span"), 2, 0, 2, 2)
    window.setLayout(layout)

    window.show()
    sys.exit(app.exec())

    # 5. Run your application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
