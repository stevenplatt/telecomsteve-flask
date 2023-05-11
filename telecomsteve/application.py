# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
# push updated deployment using 'eb deploy' from within the folder telecomsteve/

import os
from turtle import title
from flask import Flask, render_template, request, url_for
from firebase_admin import credentials, firestore, initialize_app

from static.py.newsfeed import newsfeed

application = Flask(__name__)

# Initialize Firestore DB
db = firestore.Client(project='telecomsteve')
docs = db.collection('web3-remote-jobs')

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

@application.route("/jobs", methods=["GET"])
def jobs():
    all_jobs = [doc.to_dict() for doc in docs.order_by('dateAdded', direction=firestore.Query.DESCENDING).limit(30).stream()]
    return render_template('jobs.html', jobs=all_jobs)

@application.route("/news", methods=["GET"])
def engineering():
    content = newsfeed('engineering')
    return render_template('news.html', news=content, blocked=filtered_urls, category='engineering')

@application.route("/finance", methods=["GET"])
def finance():
    content = newsfeed('finance')
    return render_template('news.html', news=content, blocked=filtered_urls, category='finance')

@application.route("/login", methods=["POST", "GET"])
def login():

    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    welcome_message = 'Type your credentials and press Enter to login.'
    error_message = 'The credentials entered are incorrect.'

    # source: https://pythonbasics.org/flask-http-methods/
    if request.method == 'POST':
        if username == request.form['name'] and password == request.form['key']:
            return render_template('index.html')
        else:
            return render_template('login.html', message=error_message)
    else:
        return render_template('login.html', message=welcome_message)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run(host='0.0.0.0', port=8080)
