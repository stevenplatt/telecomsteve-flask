import feedparser
import dateutil.parser
from urllib.parse import urlparse

def newsfeed(topic):
    if topic == 'finance':
        # a list of sources used to pull in engineering news
        # source: https://hnrss.github.io/ (a hacker news rss feed)
        urls = ['https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml',
                'https://www.cnbc.com/id/100727362/device/rss/rss.html',
                'https://decrypt.co/feed']

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
