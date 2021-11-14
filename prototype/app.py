from flask import Flask
from flask import render_template, request
from forms import EventForm
from urllib.parse import quote
import requests


import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/event_call', methods=['GET', 'POST'])
def event_call():
    form = EventForm()
    if request.method == 'POST':

        movieSearch = form.movieSearch.data
        movieSearch = quote(movieSearch, safe='/', encoding=None, errors=None)

        # params = {
        # 	'api_key': '{360f58d18e75896753cb7a0b873849a8}',
        # 	'classificationName': '{music}',
        # 	'search_query':
        # }

        #url = "https://api.themoviedb.org/3/search/movie?api_key={360f58d18e75896753cb7a0b873849a8}&language=en-US&query={movieSearch}&page=1&include_adult=false"

        response = requests.get(
            f"https://api.themoviedb.org/3/search/movie?api_key=360f58d18e75896753cb7a0b873849a8&language=en-US&query={movieSearch}&page=1&include_adult=false")

        json_res = response.json()

        if json_res["page"]["totalElements"] == 0:
            return render_template('no_results.html')
        else:
            return render_template('search_results.html', events=list(json_res["_embedded"]["events"]))
    else:
        return render_template('event_call.html', title='Find events', form=form)


@app.route('/search_results', methods=['POST'])
def search_results():
    return render_template('search_results.html', title='Display events')


@app.route("/register", methods=['POST'])
def register_user():
    try:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        birth_date = request.form.get('birth_date')
        hometown = request.form.get('hometown')
        gender = request.form.get('gender')
    except:
        # this prints to shell, end users will not see this (all print statements go to shell)
        print("couldn't find all tokens")
        return flask.redirect(flask.url_for('register'))
    cursor = conn.cursor()
    test = isEmailUnique(email)
    if test:
        print(cursor.execute("INSERT INTO Users (first_name, last_name, email, birth_date, hometown, gender,password) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')"
                             .format(first_name, last_name, email, birth_date, hometown, gender, password)))
        conn.commit()
        # log user in
        user = User()
        user.id = email
        flask_login.login_user(user)
        return render_template('profile.html', name=email, message='Account Created!')


if __name__ == '__main__':
    app.run()
