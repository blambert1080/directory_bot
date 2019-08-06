
import requests
from bs4 import BeautifulSoup
from credentials import login, urls

__DIRECTORY_URL = urls["directory_url"]
__FAMILY_URL = urls["family_url"]


session_requests = requests.session()


def login_congregate():
    LOGIN_URL = urls['login_url']
    # Login
    session_requests.get(LOGIN_URL)
    payload = {
        "username": login['username'],
        "password": login['password']
    }
    session_requests.post(
        LOGIN_URL,
        data=payload,
        headers=dict(referer=LOGIN_URL)
    )


def get_directory_page_soup():
    DASHBOARD_URL = urls["dashboard_url"]
    DIRECTORY_URL = urls["directory_url"]
    directory_page = session_requests.get(
        DIRECTORY_URL,
        headers=dict(referer=DASHBOARD_URL)
    )
    return BeautifulSoup(directory_page.content, 'html.parser')


def get_church_member_page_soup(family_link):
    DIRECTORY_URL = urls['directory_url']
    if family_link:
        FAMILY_URL = urls["family_url"] + family_link
        church_member_page = session_requests.get(
            FAMILY_URL,
            headers=dict(referer=DIRECTORY_URL)
        )
        return BeautifulSoup(church_member_page.content, 'html.parser')
    else:
        return None


login_congregate()
