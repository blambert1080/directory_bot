
import re
import requests
from bs4 import BeautifulSoup
from credentials import login, urls
from lxml import html
from urllib.request import urlopen

__USERNAME = login["username"]
__PASSWORD = login["password"]
__LOGIN_URL = urls["login_url"]
__DIRECTORY_URL = urls["directory_url"]
__DASHBOARD_URL = urls["dashboard_url"]
__FAMILY_URL = urls["family_url"]

session_requests = requests.session()

def login_congregate():
    # Login
    login_page = session_requests.get(__LOGIN_URL)
    payload = {
        "username": __USERNAME,
        "password": __PASSWORD
    }
    login_page = session_requests.post(
        __LOGIN_URL,
        data = payload,
        headers = dict(referer = __LOGIN_URL)
    )

def find_church_member_page(first_name, last_name):
    # Directory Searching
    directory_page = session_requests.get(
        __DIRECTORY_URL,
        headers = dict(referer = __DASHBOARD_URL)
    )
    directory_soup = BeautifulSoup(directory_page.content, 'html.parser')
    if last_name:
        family_query = directory_soup.find_all('h3', string=re.compile(last_name))
        if len(family_query) > 1:
            full_name_regex = "^(?=.*\\b" + last_name + "\\b)(?=.*\\b" + first_name + "\\b).*$"
            return directory_soup.find('h3', string=re.compile(full_name_regex)).find_parent('a')['href']
        else:
            return directory_soup.find('h3', string=re.compile(last_name)).find_parent('a')['href']
    else:
        family_query = directory_soup.find_all('h3', string=re.compile(first_name))
        if len(family_query) > 1:
            return None
        else:
            return directory_soup.find('h3', string=re.compile(first_name)).find_parent('a')['href']

def get_home_phone(family_soup):
    member_home = family_soup.find('strong', string=re.compile("Home Phone"))
    if member_home:
        return member_home.find_parent().select_one('a[href^="tel:"]').text.strip()
    return None

def get_cell_phone(family_soup, name, family):
    if family is True:
        family_member_cell = family_soup.find('h3', string=re.compile(name)).find_parent().select_one('a[href^="tel:"]')
        return family_member_cell.text.strip() if family_member_cell else None
    else:
        single_member_cell = family_soup.find('div', attrs={"class":"tc dir"}).find('a', string=re.compile(r"((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}"))
        return single_member_cell.text.strip() if single_member_cell else None
    return None

def get_church_member_phone(first_name, last_name):
    global __FAMILY_URL
    login_congregate()
    # split_names(name)
    first_name = first_name.capitalize()
    last_name = last_name.capitalize() if last_name else None
    church_member_query_result = find_church_member_page(first_name, last_name)
    if not church_member_query_result:
        return None
    __FAMILY_URL += church_member_query_result
    result = session_requests.get(
        __FAMILY_URL,
        headers = dict(referer = __DIRECTORY_URL)
    )
    family_soup = BeautifulSoup(result.content, 'html.parser')
    family = True if family_soup.ul else False
    home_phone = get_home_phone(family_soup)
    cell_phone = get_cell_phone(family_soup, first_name, family)
    phone_numbers = {
        "Cell" : cell_phone,
        "Home" : home_phone
    } 
    return phone_numbers