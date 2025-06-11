import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip('/')

def get_links_from_page(url, url_prefix):
    """Extract and normalize all hrefs that start with the given prefix."""
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()

        for a in soup.find_all('a', href=True):
            full_url = normalize_url(urljoin(url, a['href']))
            if full_url.startswith(url_prefix):
                links.add(full_url)

        return links
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return set()

def crawl_with_prefix(start_url, max_depth):
    start_url = normalize_url(start_url)
    prefix = start_url + '/' if not start_url.endswith('/') else start_url

    visited = set()
    result_by_level = {i: set() for i in range(max_depth + 1)}
    queue = deque([(start_url, 0)])

    while queue:
        current_url, level = queue.popleft()
        if level > max_depth or current_url in visited:
            continue

        visited.add(current_url)
        result_by_level[level].add(current_url)

        if level < max_depth:
            child_links = get_links_from_page(current_url, prefix)
            for link in child_links:
                if link not in visited:
                    queue.append((link, level + 1))

    return result_by_level[max_depth]

start_url = "https://www.thehindubusinessline.com/opinion"
depth = 2
results = crawl_with_prefix(start_url, depth)
