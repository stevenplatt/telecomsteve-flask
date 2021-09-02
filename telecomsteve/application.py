# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html

from flask import Flask
from flask import render_template, url_for, flash, redirect, request, session, abort 
from hackernews import HackerNews
import socket
import threading
import math
from urllib.parse import urlparse

application = Flask(__name__)

def get_host_ip():
    return socket.gethostbyname(socket.gethostname()) 

def news_singleton(num):
    hn = HackerNews()
    stories = hn.top_stories()
    news_dict = {"Title":[],"URL":[],"Domain":[], "Score":[]}
    try:
        website = hn.item(stories[num])

        # instructions: https://stackoverflow.com/questions/1521592/get-root-domain-of-link
        parsed_uri = urlparse(str(website.url))
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        domain = domain.replace('www.', '')

        # add story details to dictionary
        news_dict["Title"] = (str(website.title))
        news_dict["URL"] = (str(website.url))
        news_dict["Domain"] = domain
        news_dict["Score"] = (str(website.score))
    except:
        pass
    return(news_dict) 

@application.route("/")
def home():
    return render_template('index.html')


@application.route("/news", methods=["GET"])
def news():
    count = range(50) # number of stories to display
    nthreads = 50 # number 

    def worker(count, outdict):
        """ The worker function, invoked in a thread. 'nums' is a
            list of numbers to factor. The results are placed in
            outdict.
        """
        for num in count:
            outdict[num] = news_singleton(num)

    # Each thread will get 'chunksize' nums and its own output dict
    chunksize = int(math.ceil(len(count) / float(nthreads)))
    threads = []
    outs = [{} for i in range(nthreads)]

    for i in range(nthreads):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = threading.Thread(
                target=worker,
                args=(count[chunksize * i:chunksize * (i + 1)],
                      outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    output = ({k: v for out_d in outs for k, v in out_d.items()}).values()
    

    return render_template('news.html', news=output)

@application.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')

@application.route("/research")
def research():
    return render_template('research.html')

@application.route("/resume")
def resume():
    return render_template('resume.html')

@application.route("/login", methods=['POST'])
def login():
    if request.form['password'] == 'spectrum' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run(host= '0.0.0.0')
