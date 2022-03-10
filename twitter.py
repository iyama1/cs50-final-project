
import os
import pandas as pd
import json
import base64
import requests
from flask import session
import re


def twitter_conn():
    '''
    authenticate to Twitter and set header for calls
    :return:
    '''
    # open config file and get data
    with open("config.json") as config_data_file:
        config_data = json.load(config_data_file)

    twitter_data = config_data['twitter']
    session['twitter_url'] = twitter_data['base_url']

    encoded_key = b64_encoded_key(twitter_data['client_key'], twitter_data['client_secret'])

    # set variables for authorization call
    auth_url = f"{session['twitter_url']}oauth2/token"
    auth_headers = {
        'Authorization': 'Basic {}'.format(encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    auth_data = {
        'grant_type': 'client_credentials'
        }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    access_token = auth_resp.json()['access_token']

    os.environ['TWITTER_CONN'] = 'true'

    return {'Authorization': 'Bearer {}'.format(access_token)}


def b64_encoded_key(client_key, client_secret):
    '''
    :param twitter_data:
    :return str key:
    '''
    # encode key for auth call
    b64_encoded_key = '{}:{}'.format(client_key, client_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(b64_encoded_key)

    return b64_encoded_key.decode('ascii')


def get_tweets():
    '''
    retrieve tweets for twitter handle
    return: DF
    '''
    count = 200
    max = 1000
    url = f"{session['twitter_url']}1.1/statuses/user_timeline.json"
    endpoint = f"{url}?screen_name={session['handle']}&count={count}&include_rts=false&trim_user=true"

    tweet_data = requests.get(endpoint, headers=session['twitter_header'])


    tweet_json = tweet_data.json()

    df_cols = ['id','text','favorite_count', 'retweet_count']
    tweets_df = json_to_df(tweet_data.json(), df_cols)


    #tweets_df_all = pd.DataFrame(tweet_json)
    #tweets_df = tweets_df_all[['id','text','favorite_count']]

    # TODO - retrieve all tweets

    # rename column headers
    col_headers = {'id': 'ID',
                   'text': 'Tweet',
                   'favorite_count': 'Favorited',
                   'retweet_count': 'Retweets'}

    tweets_df = tweets_df.rename(columns=col_headers)

    tweets_to_text(tweets_df)

    return tweets_df


def json_to_df(input_json, columns):
    '''
    take json input and return sliced dataframe with specific columns
    :param input_json:
    :param columns:
    :return df:
    '''
    df_data = [{col: data for col, data in row.items() if col in columns} for row in input_json]

    return pd.DataFrame(df_data)


def tweets_to_text(df):
    '''
    take input df of tweets and create text block and dict for Watson APIs
    :param df:
    :return:
    '''
    # use session for tweets text and content_items?

    contentItems = {'contentItems': []}
    tweets = []

    for index, row in df.iterrows():
        # skip tweet if it's a retweet
        if row['Tweet'].find('RT', 0, 2) == 0: continue

        text = row['Tweet']

        # remove URLs
        regex = r"(https?:\/\/)(\s)*(www\.)?(\s)*((\w|\s)+\.)*([\w\-\s]+\/)*([\w\-]+)((\?)?[\w\s]*=\s*[\w\%&]*)*"

        text = re.sub(regex, '', text)

        contentItem = {
            'content': text,
            'contenttype': 'text/plain',
            'id': str(row['ID']),
            'language': 'en'
        }

        tweets.append(text)
        contentItems['contentItems'].append(contentItem)

    # reduce byte count to not exceed API limit
    tweets_text = str(tweets).replace("\'", "")

    # trim text to 128 kb - max allowed by Tone Analyzer API
    tweets_text = cut_str_to_bytes(tweets_text, 128000)

    session['tweets_text'] = tweets_text
    session['tweets_content'] = contentItems

    return


def cut_str_to_bytes(s, max_bytes):
    # cut it twice to avoid encoding potentially GBs of `s` just to get e.g. 10 bytes?
    # original function from zvone: https://stackoverflow.com/a/59451718
    b = s[:max_bytes].encode('utf-8')[:max_bytes]

    if b[-1] & 0b10000000:
        last_11xxxxxx_index = [i for i in range(-1, -5, -1)
                               if b[i] & 0b11000000 == 0b11000000][0]
        # note that last_11xxxxxx_index is negative

        last_11xxxxxx = b[last_11xxxxxx_index]
        if not last_11xxxxxx & 0b00100000:
            last_char_length = 2
        elif not last_11xxxxxx & 0b0010000:
            last_char_length = 3
        elif not last_11xxxxxx & 0b0001000:
            last_char_length = 4

        if last_char_length > -last_11xxxxxx_index:
            # remove the incomplete character
            b = b[:last_11xxxxxx_index]

    return b