import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

class SpotifyAPI(object):
    client_id = None
    client_secret = None
    redirect_uri = None
    token = None
    username = None
    API = None

    def __init__(self, username, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = SpotifyOAuth(client_id = self.client_id, client_secret = self.client_secret, redirect_uri = self.redirect_uri, scope='playlist-modify-public user-read-private', username=username)
        self.username = username
        self.API = spotipy.Spotify(auth_manager = self.token)


    def createPlaylist(self):
        self.API.user_playlist_create(user=username, name="CS411-Playlist", public=True)

    def addSongs(self, query):
        song_list = []
        result = self.API.search(q=query, type="track")
        song_list.append(result["tracks"]["items"][0]["uri"])

        prePlaylist = self.API.user_playlists(user=username)
        playlist = prePlaylist["items"][0]["id"]
        self.API.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=song_list)
        return (prePlaylist["items"][0]["external_urls"]["spotify"])



# client stuff, this shouldn't be here 
client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
client_secret = "9fd762547d2f4626b3b619c8688d9db2"
redirect_uri = "http://127.0.0.1:8080/"

# Example running this code
username = input("Give your username: ")
spotify = SpotifyAPI(username, client_id, client_secret, redirect_uri)
spotify.createPlaylist()
query = input("Give a song name: ")
print(spotify.addSongs(query))

