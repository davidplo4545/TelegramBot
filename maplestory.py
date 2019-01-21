import requests, re
from bs4 import BeautifulSoup


def get_latest_posts():
    '''
    Gets the latest maplestory posts from the maplestory.com
    website, returns a list of tuples that include (title, link)
    :return:
    '''
    url = 'http://maplestory.nexon.net/news'

    items = []
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    # get list of first 3 posts
    first_posts = soup.findAll("li", {"class": re.compile("news-item news-item-")})[2:5]
    for post in first_posts:
        title = post.find('h3').text.strip()
        link = ''.join([url.split('news')[0],
                        post.find('h3').find('a').get('href')])
        items.append((title, link))
    return items
