# cs50-final-project
## Table of Contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)


## General info
Demo Link: https://youtu.be/bXQFLzFXPTQ

This project is a web applications that utilizes Twitter and IBM Watson APIs to analyze a user's Tweets for Tone and Emotion.

The main page includes funcationality to retrieve Tweets for a user and display them in a table.

The Text page displays the concatenated text that is submitted to the Watson services for analysis

The Tone page displays a table of tones and scores for those that Watson scored over 0.5. It also includes a descriptive table.

The Emotion page displays a categorical polar chart and a table of scores by emotion


## Technologies
Project is created with:
* Python 3.6
    * Key packages:
        * Flask
        * Pandas
        * IBM-Watson
        * Plotly
* HTML
* CSS


## Setup
Prerequisites:
* Register as a developer on Twitter and generate secret and client keys
* Register for and IBM developer account: https://dataplatform.cloud.ibm.com/
* Add Watson Services and generate credentials for:
    * Tone Analyzer
    * Natural Language Understanding
* Update config.json with necessary values
