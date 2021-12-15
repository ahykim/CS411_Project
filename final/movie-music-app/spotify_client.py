import base64
import datetime
from urllib.parse import urlencode

import requests
import json

# Referenced from a Spotify API tutorial

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
    client_secret = "9fd762547d2f4626b3b619c8688d9db2"
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    def search(self, query):
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        query_params = urlencode({"q": query, "type": 'track'})
        return self.base_search(query_params)

    def SearchAndReturnSongJSON(self, query=None):
        if query == None:
            raise Exception("No query entered")
        song = self.search(query)
        dictionary={
            "song_name": song['tracks']['items'][0]['name'],
            "song_image": song['tracks']['items'][0]['album']['images'][0]['url'],
            "song_url": song['tracks']['items'][0]['external_urls']['spotify']
        }
        json_object = json.dumps(dictionary, indent = 4)
        with open("song.json", "w") as outfile:
            outfile.write(json_object)

# Uncomment code below to run example with our function:
# client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
# client_secret = "9fd762547d2f4626b3b619c8688d9db2"

# spotify = SpotifyAPI(client_id, client_secret)

# spotify.SearchAndReturnSongJSON({'track': 'Easy on Me'})