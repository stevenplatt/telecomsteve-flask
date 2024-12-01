# python flask application powering telecomsteve.com
# install requirements with 'pip3 install -r requirements.txt'

# example site: https://www.eddiejaoude.io/

import os
import datetime
from flask import Flask, render_template, request, url_for
from static.py.newsfeed import newsfeed

application = Flask(__name__)

# these urls are filtered because they are often behind a paywall
filtered_urls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com', 'politico.com', 'youtube.com',
                'ft.com', 'economist.com', 'reuters.com', 'washingtonpost.com', 'filtered']
filtered_terms = ['twitter', 'trump', 'roe', 'abortion', 'shooting', 'gun',
                'first mover', 'elon', 'musk', 'chatgpt', 'LLM', 'ftx', 'sbf', 
                'sam', 'supreme court', 'bitcoin', 'hiring']

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@application.route("/contact", methods=["GET"])
def contact():
    return render_template('contact.html')

@application.route("/research", methods=["GET"])
def research():
    return render_template('research.html')

@application.route("/news", methods=["GET"])
@application.route("/feeds", methods=["GET"])
@application.route("/engineering", methods=["GET"])
def engineering():
    content = newsfeed('engineering')
    return render_template('feeds.html', news=content, blocked=filtered_urls, category='engineering')

@application.route("/finance", methods=["GET"])
def finance():
    content = newsfeed('finance')
    return render_template('feeds.html', news=content, blocked=filtered_urls, category='finance')

@application.route("/web3", methods=["GET"])
def web3():
    content = newsfeed('web3')
    return render_template('feeds.html', news=content, blocked=filtered_urls, category='web3')

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run(host='0.0.0.0', port=8080)
