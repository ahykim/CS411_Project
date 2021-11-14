from flask import Flask
from flask import render_template, request
from forms import MovieForm
from urllib.parse import quote
import requests

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
            movies = [x["original_title"] for x in json_res["results"]]
            return render_template('search_results.html', movies=movies)
    else:
        return render_template('movie_search.html', title='Movies search', form=form)

@app.route('/search_results', methods=['POST'])
def search_results():
    return render_template('search_results.html', title='Display movies')

if __name__ == '__main__':
    app.run()
