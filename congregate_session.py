
import re
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
    FAMILY_URL = urls["family_url"] + family_link
    church_member_page = session_requests.get(
        FAMILY_URL,
        headers=dict(referer=DIRECTORY_URL)
    )
    return BeautifulSoup(church_member_page.content, 'html.parser')


# def get_church_member_page(first_name, last_name):
#     # Directory Searching
#     directory_soup = get_directory_page_soup()
#     if last_name and is_more_than_one_result(directory_soup, last_name):
#         re_full_name = ("^(?=.*\\b"
#                         + last_name
#                         + "\\b)(?=.*\\b"
#                         + first_name
#                         + "\\b).*$")
#         return get_member_number(directory_soup, re_full_name)
#     else:
#         return (get_all_member_numbers(directory_soup, first_name)
#                 if is_more_than_one_result(directory_soup, first_name)
#                 else get_member_number(directory_soup, first_name))


# def is_more_than_one_result(soup, name):
#     return len(soup.find_all('h3', string=re.compile(name))) > 1


# def get_member_number(soup, name):
#     return (None if not soup.find('h3', string=re.compile(name))
#             else soup.find('h3', string=re.compile(name))
#                      .find_parent('a')['href'])


# def get_all_member_numbers(soup, name):
#     names = {}
#     index = 0
#     for name in soup.find_all('h3', string=re.compile(name)):
#         names[index] = get_member_number(soup, name.text.strip())
#         index += 1
#     return names


login_congregate()
