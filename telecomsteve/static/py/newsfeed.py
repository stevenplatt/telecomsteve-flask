import feedparser
import dateutil.parser
from urllib.parse import urlparse

# these urls are filtered because they are often behind a paywall
filtered_urls = ['twitter.com', 'bloomberg.com', 'nytimes.com', 'wsj.com',
                'ft.com', 'economist.com', 'reuters.com', 'washingtonpost.com', 'filtered']
filtered_terms = ['trump', 'roe', 'abortion', 'shooting', 'gun', 'first mover',
                'elon', 'musk', 'chatgpt', 'LLM', 'ftx', 'deal', 'deals', 'hiring']

def newsfeed(topic):
    if topic == 'finance':
        # a list of sources used to pull in engineering news
        # source: https://hnrss.github.io/ (a hacker news rss feed)
        urls = ['https://www.cnbc.com/id/100727362/device/rss/rss.html',
                'https://feeds.bbci.co.uk/news/business/rss.xml',
                'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
                'https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml']

    elif topic == 'engineering':
        # a list of sources used to pull in technology news
        urls = ['https://www.theverge.com/rss/index.xml',
                'https://hnrss.org/frontpage',
                'https://www.engadget.com/rss.xml',
                'https://www.gamespot.com/feeds/mashup/',
                'https://feeds.a.dj.com/rss/RSSWSJD.xml']
    
    elif topic == 'world':
        # a list of sources used to pull in world news
        urls = ['https://feeds.nbcnews.com/nbcnews/public/world',
                'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
                'https://feeds.bbci.co.uk/news/world/rss.xml']

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
