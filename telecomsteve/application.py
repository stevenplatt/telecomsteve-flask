# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
# push updated deployment using 'eb deploy' from within the folder telecomsteve/

import os, feedparser
import dateutil.parser
from flask import Flask, render_template, request, url_for
from urllib.parse import urlparse

application = Flask(__name__)

# these urls are filtered because they are often behind a paywall
filtered_urls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com', 'ft.com', 'economist.com', 'reuters.com']
filtered_terms = ['trump', 'roe', 'abortion', 'shooting', 'gun', 'israel', 'first mover', 'bitcoin']

filtered = filtered_urls + filtered_terms

def newsfeed(topic): # source https://waylonwalker.com/parsing-rss-python/

    if topic == 'engineering':
        # a list of sources used to pull in engineering news
        urls = ['https://hnrss.org/frontpage'] # source: https://hnrss.github.io/ (a hacker news rss feed)
    
    elif topic == 'world':
        # a list of sources used to pull in world news
        urls = ['https://www.aljazeera.com/xml/rss/all.xml',
            'https://www.cnbc.com/id/100727362/device/rss/rss.html']

    else:
        # a list of sources used to pull in technology news
        urls = ['https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml',
            'https://www.theverge.com/rss/index.xml'] # 'https://www.fiercewireless.com/rss/xml' 

    feeds = [feedparser.parse(url)['entries'] for url in urls]
    feed = [item for feed in feeds for item in feed]
    feed.sort(key=lambda x: dateutil.parser.parse(x['published']), reverse=True)

    for item in feed:
        for term in filtered:
            if term in (item['title'].lower() or item['domain'].lower()):
                feed.remove(item)
            else:
                date = item.get('published')[:-15] # remove the timestamp from the date
                item.update({'published':date})

                parsed_uri = urlparse(item.get('link')) # instructions: https://stackoverflow.com/questions/1521592/get-root-domain-of-link
                domain = '{uri.netloc}'.format(uri=parsed_uri)
                domain = domain.replace('www.', '')
                item.update({'domain': domain})
    
    return feed[:30]

@application.route("/")
def home():
    return render_template('index.html')

@application.route("/news", methods=["GET"]) 
def technology(): 
    content = newsfeed('technology')
    return render_template('news.html', news=content, blocked=filtered, category='technology')

@application.route("/engineering", methods=["GET"])
def engineering(): 
    content = newsfeed('engineering')
    return render_template('news.html', news=content, blocked=filtered, category='engineering')

@application.route("/world", methods=["GET"]) 
def world(): 
    content = newsfeed('world')
    return render_template('news.html', news=content, blocked=filtered, category='world')

@application.route("/research", methods=["GET"])
def research():
    return render_template('research.html')

@application.route("/login", methods=["POST", "GET"])
def login():

    username = os.environ['USERNAME']
    password = os.environ['PASSWORD']
    welcome_message = 'Type your credentials and press Enter to login.'
    error_message = 'The credentials entered are incorrect.'

    if request.method == 'POST': # source: https://pythonbasics.org/flask-http-methods/

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
    application.run (host= '0.0.0.0', port=8080) # (host="localhost", port=8000) #
