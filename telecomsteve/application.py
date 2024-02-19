# python flask application powering telecomsteve.com
# install requirements with 'pip3 install -r requirements.txt'

import os
import datetime
# from turtle import title
from flask import Flask, render_template, request, url_for

from static.py.newsfeed import newsfeed

application = Flask(__name__)

# these urls are filtered because they are often behind a paywall
filtered_urls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com',
                'ft.com', 'economist.com', 'reuters.com', 'washingtonpost.com', 'filtered']
filtered_terms = ['twitter', 'trump', 'roe', 'abortion', 'shooting', 'gun',
                'first mover', 'elon', 'musk', 'chatgpt', 'LLM', 'ftx', 'sbf', 
                'sam', 'supreme court', 'bitcoin', 'hiring']

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/research", methods=["GET"])
def research():
    return render_template('research.html')

@application.route("/news", methods=["GET"])
def engineering():
    content = newsfeed('engineering')
    return render_template('news.html', news=content, blocked=filtered_urls, category='engineering')

@application.route("/finance", methods=["GET"])
def finance():
    content = newsfeed('finance')
    return render_template('news.html', news=content, blocked=filtered_urls, category='finance')

@application.route("/web3", methods=["GET"])
def web3():
    content = newsfeed('web3')
    return render_template('news.html', news=content, blocked=filtered_urls, category='web3')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run(host='0.0.0.0', port=8080)
