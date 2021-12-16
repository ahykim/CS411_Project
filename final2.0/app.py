from flask import Flask
from flask import render_template, request
from forms import MovieForm, SpotifyForm
from urllib.parse import quote
import requests
import spotifyTest

import os

app = Flask(__name__)

SECRET = os.urandom(32)
app.config['SECRET_KEY'] = SECRET

@app.route('/', methods=['GET', 'POST'])
def movie_search():
    form = MovieForm()
    if request.method == 'POST':

        movieSearch = form.movieSearch.data
        movieSearch = quote(movieSearch, safe='/', encoding=None, errors=None)

        response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key=360f58d18e75896753cb7a0b873849a8&language=en-US&query={movieSearch}&page=1&include_adult=false")

        json_res = response.json()
        if json_res["total_results"] == 0:
            return render_template('no_results.html')
        else:
            movies = json_res["results"][0]
        
            # client stuff, this shouldn't be here 
            client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
            client_secret = "9fd762547d2f4626b3b619c8688d9db2"
            redirect_uri = "http://127.0.0.1:8080/"

            # Example running this code
            username = "31s5vavxp2gkfow5snvyrw5s6kya"
            spotify = spotifyTest.SpotifyAPI(username, client_id, client_secret, redirect_uri)
            spotify.createPlaylist()
            playlistInfo = spotify.addSongs(movieSearch)

            return render_template("spotify_results.html", 
                                    playlistTitle=playlistInfo["name"],
                                    playlistCover=playlistInfo["image"], 
                                    playlistUrl=playlistInfo["url"],
                                    moviePoster=movies["poster_path"],
                                    movieTitle=movies["title"],
                                    form=form)
    else:
        return render_template('movie_search.html', title='Movies search', form=form)

# @app.route('/', methods=['GET', 'POST'])
# def search_results():
#     form = SpotifyForm()
#     if request.method == 'POST':
#         spotifySearch = form.spotifySearch.data
#         spotifySearch = quote(spotifySearch, safe='/', encoding=None, errors=None)
        
#         # client stuff, this shouldn't be here 
#         client_id = "49b72ad3205148bfb5ea7922a7b9eba9"
#         client_secret = "9fd762547d2f4626b3b619c8688d9db2"
#         redirect_uri = "http://127.0.0.1:8080/"

#         # Example running this code
#         username = "31s5vavxp2gkfow5snvyrw5s6kya"
#         spotify = spotifyTest.SpotifyAPI(username, client_id, client_secret, redirect_uri)
#         spotify.createPlaylist()
#         query = spotifySearch
#         playlistInfo = spotify.addSongs(query)

#         return render_template("spotify_results.html", title=playlistInfo["name"], cover=playlistInfo["image"], url=playlistInfo["url"], form=form)
#     else:
#         return render_template('spotify_search.html', title='Display movies', form=form)

if __name__ == '__main__':
    app.run()
