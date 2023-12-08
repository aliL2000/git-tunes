# git-tunes

This project, created in Python and using PyQt, allows people to combine their Spotify playlists through a simple GUI so that they don't have to manually add each individual song to their playlists

I made this project as a sort of POC, and might explore this further? Depending on how I feel.

## Table of Contents

- [Prerequisites](#pre-requisites)
- [Getting Started](#getting-started)
- [Contact Me](#contact-me)
- [Future Development](#future-development)

## Pre-requisites

You'll need the following applications to be installed:

 1. **Python**
    
    Python is used to authenticate and update your Spotify Playlists.

    Python can be installed from [here](https://www.python.org/).

2. **Chrome**
    
    Chrome is used for authentication purposes, I might find a workaround, but deal with it for now.

    Chrome can be installed from [here](https://www.google.com/intl/en_ca/chrome/).

**NOTE**: To use the Spotify API, you can either create your own Spotify application and get your own *client_id* and *client_secret* **OR** you can contact me (see below), to get my application credentials (I need to verify your usage of the program), then you can go the .env file located in the project and copy and paste the contents within the .txt file I send you.

## Getting started

Clone the repository to your location of choice, using the following command.

```
git clone https://github.com/aliL2000/git-tunes.git
```

You'll need to run the following commands to get the prerequisite packages installed on your system. You can either run this using a virtual environement (**HIGHLY RECOMMENDED**) or just install the packages on your local system.

```
pip install -r requirements.txt
```
Then, navigate to the **/src** directory using this command:

```
cd src
```
Then, run this command to begin the program:
```
python main.py
```

## Contact Me

My name is Ali, I can be reached on my personal email [here](mailto:aliladha2000@gmail.com).


## Future Development

Some features, ordered in terms of personal priority:

- Check all songs button, essentially over-riding the one-by-one selection of each song.
- Create a .exe, thereby circumnavigating the manual authentication information exchange I have to do with any new user.