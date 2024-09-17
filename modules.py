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
    print("Extracted domain:    ", domain)

    
def set_course_id(url: str) -> None:
    """
    Extracts course ID from given URL and assigns global variable
    course_id to it. 

    Allows for easier conversion of e.g. file IDs to full urls
    """
    global course_id
    course_id_index = url.index("courses") + 8
    course_id = url[course_id_index:course_id_index+4]
    print("Extracted course ID: ", course_id)

    
def download_file(file_link) -> None:
    """
    Downloads file from file_link and saves it in Downloads subfolder
    of current working directory.
    """
    print("\tInitiating download...")
    try: 
        with page.expect_download(timeout=5000) as download_info:
            try:
                page.goto(file_link)
            except:
                pass # playwright throws an error when you try to download a pdf... by design... every time...
            download = download_info.value
            print(f"\tDownloading file: \t{download.suggested_filename}")
            # print(f"Downloading file: \t{download.suggested_filename} ({download.url})")
            download.save_as(f"./Downloads/{course_id}/{download.suggested_filename}")
    except:
        print("\t\tFile failed to download and I haven't implemented a function\n" \
            + "\t\tthat finds out why! Try clicking the URL and see what Canvas\n" \
            + "\t\thas to say about this:")
        print("\t\t\t", file_link)
        print("\t\tOr maybe your internet is slow enough to trigger the 5s\n"\
            + "\t\ttimeout I've set. ")
        print("\t\tIt's very simply to change this: just change the value of\n"\
            + "\t\t'timeout' in the download_file function")
              
        pass

def get_file_ids(page) -> list[str]:
    """
    Extracts file IDs from a page, assuming it structures its data
    similarly to the "modules" section
    """

    file_ids = []
    
    # DON'T blame me for this horror; modelling/traversing modern web
    # pages is like glimpsing weak-willed into a palantír: your sanity
    # will likely not thank you. 
    lists = page.find_all(class_="ig-list")[0].find_all("li")

    for li in lists:
        # file IDs are stored as an Attachment_{file_id} class in li 
        for class_ in li['class'][::-1]:
            if class_[0:3] == 'Att':
                file_id = class_.removeprefix("Attachment_")
                file_ids.append(file_id)

    return file_ids
                

def convert_id_to_link(file_id: str) -> str:
    """Converts a file's ID to its download link"""
    return f"{domain}/courses/{course_id}/files/{file_id}/download?download_frd=1"


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("moron. lol.")
        exit()

    url = sys.argv[1]
    set_domain(url)
    set_course_id(url)

    with sync_playwright() as p:

        print("Setting up Playwright to do... stuff!")
        global context, page
        browser = p.firefox.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        load_cookies(context, './cookies.json')

        print("Doing... stuff!")
        print("\tGetting page content")
        page_html = get_page(url)
        page_soup = BeautifulSoup(page_html, features='html.parser')
        print("\tExtracting file IDs from html...")
        file_ids = get_file_ids(page_soup)
        print(f"Found {len(file_ids)} files!") 

        print("\tDownloading files...")
        for file_id in file_ids:
            file_link = convert_id_to_link(file_id)
            download_file(file_link)
            


