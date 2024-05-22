# python flask application powering telecomsteve.com
# install requirements with 'pip3 install -r requirements.txt'

# example site: https://www.eddiejaoude.io/

import os
import datetime
from flask import Flask, render_template, url_for

application = Flask(__name__)

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

@application.route("/consulting", methods=["GET"])
def consulting():
    return render_template('meetings/consulting.html')

@application.route("/interview-30", methods=["GET"])
def interview_30():
    return render_template('meetings/interview_30.html')

@application.route("/interview-60", methods=["GET"])
def interview_60():
    return render_template('meetings/interview_60.html')

@application.route("/news", methods=["GET"])
@application.route("/feeds", methods=["GET"])
@application.route("/engineering", methods=["GET"])
def engineering():
    return render_template('feeds.html', category='engineering')

@application.route("/finance", methods=["GET"])
def finance():
    return render_template('feeds.html', category='finance')

@application.route("/web3", methods=["GET"])
def web3():
    return render_template('feeds.html', category='web3')

if __name__ == "__main__":
    application.debug = False
    application.run(host='0.0.0.0', port=8080)
