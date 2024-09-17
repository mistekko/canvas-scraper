from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json, sys, os


def load_cookies(context, cookies_file) -> None:
    """Adds cookies in cookie_file to passed context"""
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)
    context.add_cookies(cookies)


def get_page(url: str) -> str:
    """
    Downloads and returns the source HTML for specified web page
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
    links = get_links(page)
    print(f"Found {len(links)} links")

    for link in links:
        if is_folder(link):
            folders.append(domain + link)
        else:
            files.append(link)

    return files, folders


def set_domain(url: str) -> None:
    """
    Extracts domain from given url and assigns global variable domain to
    it. 

    This is necessary because the sub-folder links gathered by this
    scraper are absolute paths, not complete URLs. To complete the
    paths by turning them into URLs, we simply prepend the site's
    Domain.
    """
    global domain
    domain_end_index = url.index("courses")-1
    domain = url[0:domain_end_index]
    print("Extracted domain: ", domain)

    
def get_course_id(url: str) -> None:
    """
    Extracts course ID from given URL and assigns global variable
    course_id to it. 

    Allows for easier conversion of e.g. file IDs to full urls
    """
    global course_id
    course_id_index = url.index("courses") + 8
    course_id = url[course_id_index:course_id_index+4]
    print(course_id)

    
def get_download(file_link):
    with page.expect_download() as download_info:
        try:
            page.goto(file_link)
        except:
            pass # playwright throws an error when you try to download a pdf... intentionally... every time...
    download = download_info.value
    print(f"Downloading file: \t{download.suggested_filename}")
    # print(f"Downloading file: \t{download.suggested_filename} ({download.url})")
    download.save_as("./Downloads/" + download.suggested_filename)

         
if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("moron. lol.")
        exit()

    url = sys.argv[1]
    set_domain(url)

    folders = [url]
    files = []

    with sync_playwright() as p:

        global context, page
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        load_cookies(context, './cookies.json')

        for folder in folders:
            print(f"Entering folder: {folder}")
            results = get_sorted_links(folder)
            print(f"{len(results[0])} new files and {len(results[1])} new folders")
            files += results[0]
            folders += results[1]
            folders.pop(0)

        print(f"Total files found: {len(files)}")

        os.makedirs("./downloads", exist_ok=True)
            
        for file_link in files:
            get_download(file_link)

        page.close()
        browser.close()




        
