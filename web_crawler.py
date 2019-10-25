import requests
from bs4 import BeautifulSoup
import pprint
from urllib.parse import urlparse, urljoin
import os
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt




def parse_page(url):
    
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    main_page = soup.find(id = 'bodyContent')
    return main_page


def get_links(soup):
    links = []
    for link in soup.find_all('a'):
        hrefs = link.get('href')
        if hrefs is not None and hrefs[0] != '#' and test_url(hrefs) is True:
            links.append(hrefs)
    return links



def test_url(url):
    whitelist = ['', '.html', '.htm']
    parsed_url = urlparse(url)
    path = parsed_url.path
    ext = os.path.splitext(path)[1]

    if ext not in whitelist:
        return False

    if path == False:
        return False

    if '/Category:' in path:
        return False

    if '/Help:' in path:
        return False

    if '/Special:' in path:
        return False

    # r = requests.get(url)
    # if r.status_code != 200:
    #     return False

    return True




def get_clean_urls(list_of_urls):
    clean = []
    host = 'https://en.wikipedia.org'
    for url in list_of_urls:
        link = urlparse(url)
        url = urljoin(host, link.path)
        if '/wiki/' in url and test_url(url):
            clean.append(url)
    return clean



def scrape(url):
    
    soup = parse_page(url)
    links = get_links(soup)
    clean_urls = get_clean_urls(links)
    return clean_urls


def crawl_depth_first(url, done, max_depth = 2, depth = 0):
    if depth < max_depth:
        for link in scrape(url):
            if link not in done:
                done.add(link)
            crawl_depth_first(link, done, max_depth, depth+1)


def crawl_with_queue(url, max_depth = 2, depth = 0):

    link_queue = [(url, depth)]
    links = set()

    while len(link_queue) > 0:

        item = link_queue.pop(0)
        url = item[0]
        depth = item[1]
        links.add(url)

        if depth < max_depth:
            for link in scrape(url):
                link_queue.append((link, depth + 1))
    return links


############################################################################
#######                  RANDOM SAMPLES
############################################################################

def scrape_random(url):
    
    soup = parse_page(url)
    links = get_links(soup)
    clean_urls = get_clean_urls(links)
    rand = np.random.choice(clean_urls, 2)
    return list(rand)



def random_crawl_with_queue(url, max_depth = 5, depth = 0):

    link_queue = [(url, depth)]
    links = set()
    link_connections = list()

    while len(link_queue) > 0:

        item = link_queue.pop(0)
        url = item[0]
        depth = item[1]
        links.add(url)

        if depth < max_depth:
            for link in scrape_random(url):
                link_queue.append((link, depth + 1))
                link_connections.append((url, link))
    return links, link_connections
                


def random_crawl_depth_first(url, done, max_depth = 10, depth = 0):
    if depth < max_depth:
        for link in scrape_random(url):
            if link not in done:
                done.add(link)
            crawl_depth_first(link, done, max_depth, depth+1)









# time recursive depth first

# start_recursion = time.time()
# done = set()

# random_crawl_depth_first('https://en.wikipedia.org/wiki/Router_(computing)', done)
# end_recursion = time.time()

# print(end_recursion - start_recursion)


# time queue breadth first

# start_queue = time.time()

x = random_crawl_with_queue('https://en.wikipedia.org/wiki/Router_(computing)')

# print(x[1])

# end_queue = time.time()

# print(end_queue - start_queue)


# visualize_data

def visualize(lst):
    g = nx.Graph()
    for i in lst:
        g.add_node(i[0])
    for i in lst:
        g.add_edge(i[0],i[1])

    nx.draw(g)
    plt.savefig("wikipedia.png") # save as png


    # print(g.nodes)
    # print(g.edges)



# print(done)


# with open('links.txt', 'w') as f:
#     for item in done:
#         f.write("%s\n" % item)


visualize(x[1])