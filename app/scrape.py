import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import errno
import re

def create_directory(path):
    """Create directory if it doesn't exist."""
    try:
        os.makedirs(path)
    except FileExistsError as e:
        raise FileExistsError(f"The directory '{path}' already exists.") from e
    
def get_filename_from_url(url):
    """Extract filename from URL."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        return 'index'
    return filename

def download_file(session, url, save_path):
    """Download a file from a URL and save it to the specified path."""
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url} -> {save_path}")
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")

def fetch_website_source(url):
    """Fetch HTML, CSS, JS, and images from a website and save them locally."""
    match = re.search(r'(?:https?:\/\/)?(?:www\.)?([^\/]+)\/', url)
    website_name = match.group(1)

    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'})

    # Create output directories
    try:
        create_directory(website_name)
    except FileExistsError as e:
        print(f"Directory {website_name} already exists")
        return
    css_dir = os.path.join(website_name, 'css')
    js_dir = os.path.join(website_name, 'js')
    images_dir = os.path.join(website_name, 'images')
    create_directory(css_dir)
    create_directory(js_dir)
    create_directory(images_dir)

    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        html_content = response.text
        with open(os.path.join(website_name, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Saved HTML to {os.path.join(website_name, 'index.html')}")
    except requests.RequestException as e:
        print(f"Failed to retrieve HTML from {url}: {e}")
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # Download CSS files
    for link_tag in soup.find_all('link', rel='stylesheet'):
        css_href = link_tag.get('href')
        if css_href:
            css_url = urljoin(url, css_href)
            css_filename = get_filename_from_url(css_url)
            if not css_filename.endswith('.css'):
                css_filename += '.css'
            save_path = os.path.join(css_dir, css_filename)
            download_file(session, css_url, save_path)

    # Download JS files
    for script_tag in soup.find_all('script'):
        js_src = script_tag.get('src')
        if js_src:
            js_url = urljoin(url, js_src)
            js_filename = get_filename_from_url(js_url)
            if not js_filename.endswith('.js'):
                js_filename += '.js'
            save_path = os.path.join(js_dir, js_filename)
            download_file(session, js_url, save_path)

    # Download Images
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src')
        if img_src:
            img_url = urljoin(url, img_src)
            img_filename = get_filename_from_url(img_url)
            save_path = os.path.join(images_dir, img_filename)
            download_file(session, img_url, save_path)

    print("Website source code has been downloaded successfully.")

if __name__ == '__main__':
    fetch_website_source('https://www.sliverpizzeria.com/')