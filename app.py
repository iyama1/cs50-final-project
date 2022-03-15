import os
from flask import Flask, session, render_template, redirect, request, flash
from flask_session import Session
#from flask_session.__init__ import Session
from tempfile import mkdtemp
import requests
import pandas as pd
from .twitter import twitter_conn, get_tweets
from .watson_apis import watson_conn, analyze_tone

# configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

os.environ['TWITTER_CONN'] = 'false'

#set_env_variables()

#twitter_header = authenticate_twitter(os.environ['TWITTER_KEY'])


@app.route("/", methods=["GET", "POST"])
def index():
    """ main page """

    if request.method == "POST":

        if os.environ['TWITTER_CONN'] == 'false':
            flash('please connect to Twitter')

            return redirect("/")

        session['handle'] = request.form.get('handle')

        #endpoint = os.environ['TWITTER_URL'] + '1.1/users/show.json?screen_name=' + session['handle']
        endpoint = f"{session['twitter_url']}1.1/users/show.json?screen_name={session['handle']}"

        user_info = requests.get(endpoint, headers=session['twitter_header'])
        user_json = user_info.json()
        session['tweet_count'] = user_json['statuses_count']

        tweets = get_tweets()

        return render_template("index.html", screen_name=session['handle'], tweet_count=session['tweet_count'], tweets=tweets)

    else:
        return render_template("index.html")


@app.route("/twitter", methods=["GET", "POST"])
def connect_twitter():
    session['twitter_header'] = twitter_conn()

    return redirect("/")

@app.route("/watson", methods=["GET", "POST"])
def connect_watson():
    watson_conn()

    return redirect("/")


@app.route("/text", methods=["GET"])
def show_text():
    # print('tweets_content type: ' + str(type(session['tweets_content'])))
    # print('contentItems type: ' + str(type(session['tweets_content']['contentItems'])))

    return render_template("text.html")

@app.route("/tone", methods=["GET"])
def tone_analysis():
    # if text data is available then analyze and show
    if request.method == "POST":
        # if text is not available to analyze then flash error
        if not session.get('tweets_text'):
            flash('Tweet text data not available to analyze')
            render_template("tone.html")

        tone_analysis = analyze_tone()

        tone_df = pd.DataFrame(tone_analysis['document']['tones'])

        render_template("tone.html", tone_df=tone_df)

    else:
        render_template("tone.html")

if __name__ == '__main__':
    app.run()