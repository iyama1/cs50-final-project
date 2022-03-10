import json
from flask import session
import requests
import pandas as pd
from ibm_watson import ToneAnalyzerV3, PersonalityInsightsV3, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def watson_conn():
    '''
    set session variables authenticators and versions for Watson calls
    :return:
    '''
    # open config file and get data
    with open("config.json") as config_data_file:
        config_data = json.load(config_data_file)

    tone_data = config_data['watson']['tone_api']
    personality_data = config_data['watson']['personality_api']

    # set session URLs
    session['personality_url'] = personality_data['url']

    # set Watson Authenticators
    session['personality_auth'] = IAMAuthenticator(personality_data['apikey'])

    # set API versions for requests
    session['personality_version'] = personality_data['version']

    session['tone_analyzer'] = ToneAnalyzerV3(
        version=tone_data['version'],
        authenticator=IAMAuthenticator(tone_data['apikey'])
    )

    #session['tone_analyzer'].set_service_url(tone_data['url'])

    return


def analyze_tone():

    # TODO - use tweets_text

    # run tone analysis on tweets_text set in twitter.tweets_to_text()

    tone_analysis = session['tone_analyzer'].tone(
        {'text': session['tweets_text']},
        content_type='application/json',
        sentences=False
    ).get_result()

    print(json.dumps(tone_analysis, indent=2))

    return tone_analysis