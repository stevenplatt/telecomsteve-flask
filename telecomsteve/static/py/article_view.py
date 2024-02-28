import requests
from readabilipy import simple_json_from_html_string

def article(url):
    req = requests.get(url)
    article = simple_json_from_html_string(req.text, use_readability=True)
    title = article['title']
    byline = article['byline']
    content = article['plain_text']
    return title, byline, content