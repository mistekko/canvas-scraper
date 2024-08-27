from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import sys




def load_cookies(context, cookies_file) -> None:
    """Adds cookies in cookie_file to passed context"""
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)
    context.add_cookies(cookies)

# def get_file(url: str) -> None
# """Downloads file from *url*

def get_page(url: str) -> str:
    """
    Downloads the source HTML for specified web page
    i.e, for URL extracting
    """        
    page.goto(url)
    page.wait_for_load_state('networkidle')
    
    return page.content()

    
def get_links(page: str) -> list:
    """
    Returns a list containing the links attached to each file listed in
    "files" page on canvas. Assumes *page* is the source code for a canvas
    directory.
    """
    soup = BeautifulSoup(page, features="html.parser")
    divs = soup.find_all(class_="ef-name-col__link")
    
    links = [a["href"] for a in divs]

    return links


def is_folder(link: str) -> bool:
    """
    Returns True if a link taken from a canvas directory page is a link
    to another directory and False otherwise.
    """
    return link[0] == "/"


def get_sorted_links(url: str) -> list[list]:
    """
    Grabs links from canvas directory, sorts them, and returns their
    sorted lists.
    """
    folders = []
    files = []

    page = get_page(url)
    with open(page) as file:
        page = file.read()

    links = get_links(page)

    for link in links:
        if is_folder(link):
            print("found folder:", link)
            folders.append(domain + link)
        else:
            print("found file:", link)
            files.append(link)

    return files, folders

def set_domain(url: str) -> None:
    """
    Extracts domain from given url and assigns global variable domain to
    it. Returns nothing.

    This is necessary because the sub-folder links gathered by this
    scraper are absolute paths, not complete URLs. To complete the
    paths by turning them into URLs, we simply prepend the site's
    Domain.
    """
    global domain
    domain_end_index = url.index("courses")-1
    domain = url[0:domain_end_index]
    print("Extracted domain: ", domain)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("moron. lol.")
        exit()

    url = sys.argv[1]
    set_domain(url)

    folders = [url]
    files = []

    p = sync_playwright()

    global browser, context, page
    browser = p.firefox.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    load_cookies(context, './cookies.json')
    
    for folder in folders:
           results = get_sorted_links(folder)
           files += results[0]
           folders += results[1]
           folders.pop(0)
    print(files)
    p.close

# https://illinoiswesleyan.instructure.com/courses/3940/files
