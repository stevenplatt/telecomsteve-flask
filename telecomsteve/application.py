# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
# push updated deployment using 'eb deploy' from within the folder telecomsteve/

import os
import feedparser
from turtle import title
import dateutil.parser
from flask import Flask, render_template, request, url_for
from urllib.parse import urlparse

application = Flask(__name__)

# these urls are filtered because they are often behind a paywall
filtered_urls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com',
                 'ft.com', 'economist.com', 'reuters.com', 'washingtonpost.com', 'filtered']
filtered_terms = ['trump', 'roe', 'abortion', 'shooting', 'gun',
                  'first mover', 'elon', 'musk', 'tesla', 'supreme court', 'bitcoin', 'hiring']


def newsfeed(topic):  # source https://waylonwalker.com/parsing-rss-python/

    if topic == 'finance':
        # a list of sources used to pull in engineering news
        # source: https://hnrss.github.io/ (a hacker news rss feed)
        urls = ['https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml',
                'https://www.cnbc.com/id/100727362/device/rss/rss.html']

    # elif topic == 'world':
        # a list of sources used to pull in world news
        # urls = ['https://www.aljazeera.com/xml/rss/all.xml',
        # 'https://www.cnbc.com/id/100727362/device/rss/rss.html']

    else:
        # a list of sources used to pull in technology news
        # 'https://www.fiercewireless.com/rss/xml'
        urls = ['https://www.theverge.com/rss/index.xml',
                'https://hnrss.org/frontpage']

    feeds = [feedparser.parse(url)['entries'] for url in urls]
    feed = [item for feed in feeds for item in feed]
    feed.sort(key=lambda x: dateutil.parser.parse(
        x['published']), reverse=True)

    for item in feed:
        # remove the timestamp from the date
        date = item.get('published')[:-15]
        item.update({'published': date})

        # instructions: https://stackoverflow.com/questions/1521592/get-root-domain-of-link
        parsed_uri = urlparse(item.get('link'))
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        domain = domain.replace('www.', '')
        item.update({'domain': domain})

        for term in filtered_terms:
            if term.lower() in str(item.get('title')).lower():
                item.update({'domain': 'filtered'})

    return feed[:30]


@application.route("/")
def home():
    return render_template('index.html')


@application.route("/radio")
def radio():
    return render_template('radio.html')


@application.route("/news", methods=["GET"])
def technology():
    content = newsfeed('technology')
    return render_template('news.html', news=content, blocked=filtered_urls, category='technology')


@application.route("/engineering", methods=["GET"])
def engineering():
    content = newsfeed('engineering')
    return render_template('news.html', news=content, blocked=filtered_urls, category='engineering')


@application.route("/world", methods=["GET"])
def world():
    content = newsfeed('world')
    return render_template('news.html', news=content, blocked=filtered_urls, category='world')


@application.route("/finance", methods=["GET"])
def finance():
    content = newsfeed('finance')
    return render_template('news.html', news=content, blocked=filtered_urls, category='finance')


@application.route("/research", methods=["GET"])
def research():
    return render_template('research.html')


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
    # (host="localhost", port=8000) #
    application.run(host='0.0.0.0', port=8080)
