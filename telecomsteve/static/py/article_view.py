import requests
from readabilipy import simple_json_from_html_string

def article(url):
    req = requests.get(url)
    article = simple_json_from_html_string(req.text, use_readability=True)
    title = article['title']
    byline = article['byline']
    content = article['content']
    plain_text = article['plain_text']
    plain_content = article['plain_content']
    return title, byline, content, plain_text, plain_content