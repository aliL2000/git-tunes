from scripts.authorization.spotify_auth import get_authorization_code, get_new_token
from scripts.spotify_api.playlist_data import (
    get_playlist_by_id,
    get_songs_from_playlist,
    get_differences,
    add_to_playlist,
    get_playlist_id,
)
from scripts.authorization.user_authentication import obtain_spotify_redirect
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
    QMessageBox,
)
import sys


class SongApp(QWidget):
    def __init__(self):
        super().__init__()

        # Sample dictionary of songs
        self.songs = {}
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
        self.setGeometry(300, 300, 700, 500)
        self.setWindowTitle("Git-Tunes")

    def on_submit_playlists(self):
        playlist_to_copy_URL = self.playlist_to_copy.text()
        playlist_to_be_copied_URL = self.playlist_to_be_copied.text()

        playlist_to_copy_ID = get_playlist_id(playlist_to_copy_URL)
        playlist_to_copied_ID = get_playlist_id(playlist_to_be_copied_URL)

        json_first_playlist = get_playlist_by_id(self.token, playlist_to_copy_ID)
        json_second_playlist = get_playlist_by_id(self.token, playlist_to_copied_ID)

        if "error" in json_first_playlist or "error" in json_second_playlist:
            print(
                "Looks like we could not find the playlist you had in mind, re-try the link"
            )
        else:
            self.songs = get_differences(
                get_songs_from_playlist(json_first_playlist),
                get_songs_from_playlist(json_second_playlist),
            )
            self.populate_song_list()

    def populate_song_list(self):
        for song in self.songs.items():
            # Create a custom QListWidgetItem
            item = QListWidgetItem(self.song_list_widget)
            self.song_list_widget.addItem(item)

            # Create a QCheckBox
            title = song[1]["title"]
            artists = ",".join(song[1]["artist"])
            checkbox = QCheckBox(f"{title} - {artists}")
            checkbox.setChecked(False)
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
        result_status = add_to_playlist(
            self.token, get_playlist_id(self.playlist_to_be_copied.text()), self.songs
        )
        self.show_popup(result_status)

    def show_popup(self, result_status_code):
        message_box = QMessageBox()

        if result_status_code == 201:
            message_box.setIcon(QMessageBox.Icon.Information)
            message_box.setText("Songs added successfully!")
            combine_another_button = message_box.addButton(
                "Combine another set of playlists", QMessageBox.ButtonRole.ActionRole
            )
            combine_another_button.clicked.connect(self.combine_another_playlists)
        elif result_status_code == 429:
            message_box.setIcon(QMessageBox.Icon.Warning)
            message_box.setText("App Error\nContact Developer on Git Page")
        else:
            message_box.setIcon(QMessageBox.Icon.Warning)
            message_box.setText("Spotify Error\nPlease retry.")
            combine_same_button = message_box.addButton(
                "Retry", QMessageBox.ButtonRole.ActionRole
            )
            combine_same_button.clicked.connect(self.retry_adding)

        close_button = message_box.addButton("Close", QMessageBox.ButtonRole.AcceptRole)
        close_button.clicked.connect(self.close_application)

        message_box.setWindowTitle("Status")
        message_box.exec()

    def retry_adding(self):
        result_status = add_to_playlist(
            self.token, get_playlist_id(self.playlist_to_be_copied.text), self.songs
        )
        self.show_popup(result_status)

    def close_application(self):
        sys.exit(app.exec())

    def combine_another_playlists(self):
        # Implement logic to reset fields and perform any other necessary actions
        print("Combine another set of playlists clicked")
        self.playlist_to_copy.clear()
        self.playlist_to_be_copied.clear()
        self.songs.clear()
        self.populate_song_list()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = SongApp()
    form.show()
    sys.exit(app.exec())


# https://realpython.com/pysimplegui-python/#packaging-your-pysimplegui-application-for-windows
