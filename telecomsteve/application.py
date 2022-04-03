# Instructions for deployment to AWS Elastic Beanstalk
# https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html
# push updated deployment using 'eb deploy' from within the folder telecomsteve/

from email import message
import os
import threading, math, requests
import arxivpy
from unittest import result
from flask import Flask, render_template, request, url_for
from urllib.parse import urlparse
from hackernews import HackerNews


application = Flask(__name__)

@application.route("/")
def home():
    return render_template('index.html')

# @application.route("/portfolio")
# def portfolio():
#     return render_template('portfolio.html')

@application.route("blockchain") # this route is incomplete
def blockchain():

    blockchain_news = [ # a list of sources used to pull in blockchain news
        'https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml',
        'https://cointelegraph.com/rss',
        'https://www.cryptoknowmics.com/rss-feeds/news',
        'https://www.cryptoknowmics.com/rss-feeds/top-picks'
    ]

    return render_template('blockchain.html')

@application.route("/research", methods=["POST", "GET"])
def research():

    if request.method == 'POST': # source: https://pythonbasics.org/flask-http-methods/
        query = request.form['search-query'] # get form input
        clean_query = query.replace(" ", "+") # replace spaces within input
        papers = arxivpy.query(search_query=f'all:{clean_query}&start=0&max_results=20', sort_by='relevance') # return results
        
        for item in papers: # show only the date and not the time with results
            date = item.get('publish_date').date()
            item.update({'publish_date': date})
            abstract = item.get('abstract')[:500] # get only the first 500 charecters of the abstract
            item.update({'abstract': abstract})

        return render_template('research_results.html', results=papers, query=query)

    else:
        return render_template('research_main.html')

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

@application.route("/resume")
def resume():
    return render_template('resume.html')

@application.route("/blog", methods=["GET"])
def blog():

    url = f"https://api.github.com/users/stevenplatt/gists" # url to request
    blog_data = requests.get(url).json() # make the request and return the json

    return render_template('blog.html', blog=blog_data)

@application.route("/news", methods=["GET"])
def news():
    # list of domains and titles to filter from the news feed
    blocked_terms = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com', 
                    'ft.com', 'trump', 'hiring', 'economist.com', 'reuters.com']
    count = range(50) # number of stories to display
    nthreads = 50 # number 

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
            
            if len(domain) > 23: 
                domain = domain[:20] + '...' # get the first 20 charecters of the URL and append '...'
            else:
                pass

            # add story details to dictionary
            news_dict["Title"] = (str(website.title))
            news_dict["URL"] = (str(website.url))
            news_dict["Domain"] = domain
            news_dict["Score"] = (str(website.score))
        except:
            pass
        
        return(news_dict)

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
                args=(count[chunksize * i:chunksize * (i + 1)], outs[i]))
        threads.append(t)
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Merge all partial output dicts into a single dict and return it
    output = ({k: v for out_d in outs for k, v in out_d.items()}).values()

    return render_template('news.html', news=output, blocked=blocked_terms)

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = False
    application.run  (host= '0.0.0.0', port=8080) # (host="localhost", port=8000) # # #  #  # 
