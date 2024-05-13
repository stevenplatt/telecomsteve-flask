import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the title of the webpage
    title = soup.title.string

    # Extract all the links on the webpage
    links = soup.find_all("a")
    link_list = [link.get("href") for link in links]

    # Extract all the paragraphs on the webpage
    paragraphs = soup.find_all("p")
    paragraph_list = [paragraph.get_text() for paragraph in paragraphs]

    # Extract all the images on the webpage
    images = soup.find_all("img")
    image_list = [image.get("src") for image in images]

    return title, link_list, paragraph_list, image_list