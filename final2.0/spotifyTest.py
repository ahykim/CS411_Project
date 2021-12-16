import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

#username = '5u2ri8pet9jmvyh9gu66olpxy'

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
        self.username = username
        self.token = SpotifyOAuth(client_id = self.client_id, 
                                  client_secret = self.client_secret, 
                                  redirect_uri = self.redirect_uri, 
                                  scope='playlist-modify-public playlist-modify-private user-read-private ugc-image-upload', 
                                  username=username)
        self.API = spotipy.Spotify(auth_manager = self.token)


    def createPlaylist(self):
        self.API.user_playlist_create(user=self.username, name="CS411-Playlist", public=True)

    def addSongs(self, query):
        song_list = []
        result = self.API.search(q=query, type="track")
        song_list.append(result["tracks"]["items"][0]["uri"])

        prePlaylist = self.API.user_playlists(user=self.username)
        playlist = prePlaylist["items"][0]
        self.API.user_playlist_add_tracks(user=self.username, playlist_id=playlist["id"], tracks=song_list)

        # Opens, reads, and uploads base64 of placeholder playlist image
        f = open('no_song.txt', 'r', encoding='utf-8-sig')
        image = f.read().rstrip()
        self.API.playlist_upload_cover_image(playlist_id=playlist["id"], image_b64=image)
        
        # Create and output JSON with playlist name, image, and url
        cover_image = self.API.playlist_cover_image(playlist["id"])
        dictionary = {
            "name": playlist['name'],
            "image": cover_image[0]["url"],
            "url": playlist['external_urls']['spotify']
        }
        # json_object = json.dumps(dictionary, indent = 4)
        # with open("playlist.json", "w") as outfile:
        #     outfile.write(json_object)
        f.close()
        return dictionary



# # client stuff, this shouldn't be here 
# client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
# client_secret = "9fd762547d2f4626b3b619c8688d9db2"
# redirect_uri = "http://127.0.0.1:8080/"

# # Example running this code
# username = input("Give your username: ")
# spotify = SpotifyAPI(username, client_id, client_secret, redirect_uri)
# spotify.createPlaylist()
# query = input("Give a song name: ")
# spotify.addSongs(query)

