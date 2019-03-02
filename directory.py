import congregate_session
import re


DATE_RE = "^[0-9]{2}\/[0-9]{2}"
CELL_QUERY = 'a[href^="tel:"]'
EMAIL_QUERY = 'a[href^="mailto:"]'


def get_church_member_page(first_name, last_name):
    # Directory Searching
    directory_soup = congregate_session.get_directory_page_soup()
    if last_name and is_more_than_one_result(directory_soup, last_name):
        full_name_re = ("^(?=.*\\b"
                        + last_name
                        + "\\b)(?=.*\\b"
                        + first_name
                        + "\\b).*$")
        return get_member_number(directory_soup, full_name_re)
    else:
        return (get_all_member_numbers(directory_soup, first_name)
                if is_more_than_one_result(directory_soup, first_name)
                else get_member_number(directory_soup, first_name))


def get_church_member_info(first_name, last_name):
    member_results = get_church_member_page(first_name, last_name)
    matched_member_info = {}
    if type(member_results) is dict:
        for link in member_results:
            matched_member_info[link] = process_results(member_results[link])
    else:
        return process_results(member_results)
    print(matched_member_info)
    return matched_member_info


# ************************* HELPER FUNCTIONS ****************************
def process_results(family_link):
    family_soup = (congregate_session
                   .get_church_member_page_soup(family_link))
    return (process_family_members(family_soup) if family_soup.li
            else process_single_members(family_soup))


def is_more_than_one_result(soup, name):
    return len(soup.find_all('h3', string=re.compile(name))) > 1


def get_member_number(soup, name):
    return (None if not soup.find('h3', string=re.compile(name))
            else soup.find('h3', string=re.compile(name))
                     .find_parent('a')['href'])


def get_all_member_numbers(soup, name):
    names = {}
    for name in soup.find_all('h3', string=re.compile(name)):
        names[strip_tag(name)] = get_member_number(soup, strip_tag(name))
    return names


# TODO: Add Address
def process_family_members(soup):
    family_members = {}
    adress = "hello"
    anniversary = get_family_date(soup, "Anniversary")
    home_phone = strip_tag(soup.find('strong', string=re.compile("Home"))
                           .find_parent('p').select_one('p a'))
    for index, member in enumerate(soup.select('li')):
        email = strip_tag(member.select_one(EMAIL_QUERY))
        cell_phone = get_family_cell_phone(member)
        birthday = get_family_date(member, "Birthday")
        anniversary = None if index > 1 else anniversary
        family_members[strip_tag(member.h3)] = {
            "address": address,
            "home_phone": home_phone,
            "email": email,
            "cell_phone": cell_phone,
            "birthday": birthday,
            "anniversary": anniversary
        }
    return family_members


# TODO: Fix Address
def process_single_members(soup):
    name = " ".join(strip_tag(soup.body.div.div.h1).split(', ')[::-1])
    address = "hello"
    email = strip_tag(soup.select_one(EMAIL_QUERY))
    cell_phone = get_single_cell_phone(soup)
    home_phone = strip_tag(soup.find('strong', string=re.compile("Home"))
                           .find_parent('p').select_one('p a'))
    birthday = strip_tag(soup.find('p', string=re.compile(DATE_RE)))
    single_member = {}
    single_member[name] = {
        "address": address,
        "home_phone": home_phone,
        "email": email,
        "cell_phone": cell_phone,
        "birthday": birthday,
    }
    return single_member


def get_family_date(soup, date):
    date_tag = soup.find('dt', string=re.compile(date))
    return (strip_tag(date_tag.find_next_sibling('dd')) if date_tag
            else None)


def get_single_cell_phone(soup):
    cell_phone = soup.find('h4', string=re.compile("Cell"))
    return (
            None if not cell_phone
            else strip_tag(cell_phone.find_next_sibling('p').select_one('p a'))
           )


def get_family_cell_phone(soup):
    return strip_tag(soup.select_one(CELL_QUERY))


def strip_tag(tag):
    return None if not tag else tag.text.strip()


print(get_church_member_info('Carlos', None))



# __USERNAME = login["username"]
# __PASSWORD = login["password"]
# __LOGIN_URL = urls["login_url"]
# __DIRECTORY_URL = urls["directory_url"]
# __DASHBOARD_URL = urls["dashboard_url"]
# __FAMILY_URL = urls["family_url"]

# session_requests = requests.session()


# # def login_congregate():
# #     # Login
# #     login_page = session_requests.get(__LOGIN_URL)
# #     payload = {
# #         "username": __USERNAME,
# #         "password": __PASSWORD
# #     }
# #     login_page = session_requests.post(
# #         __LOGIN_URL,
# #         data=payload,
# #         headers=dict(referer=__LOGIN_URL)
# #     )

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

# # def find_church_member_page(first_name, last_name):
# #     # Directory Searching
# #     directory_page = session_requests.get(
# #         __DIRECTORY_URL,
# #         headers=dict(referer=__DASHBOARD_URL)
# #     )
# #     directory_soup = BeautifulSoup(directory_page.content, 'html.parser')
# #     if last_name:
# #         family_query = directory_soup.find_all('h3', string=re.compile(last_name))
# #         if len(family_query) > 1:
# #             full_name_regex = "^(?=.*\\b" + last_name + "\\b)(?=.*\\b" + first_name + "\\b).*$"
# #             return directory_soup.find('h3', string=re.compile(full_name_regex)).find_parent('a')['href']
# #         else:
# #             return directory_soup.find('h3', string=re.compile(last_name)).find_parent('a')['href']
# #     else:
# #         family_query = directory_soup.find_all('h3', string=re.compile(first_name))
# #         if len(family_query) > 1:
# #             return None
# #         else:
# #             return directory_soup.find('h3', string=re.compile(first_name)).find_parent('a')['href']


# def get_home_phone(family_soup):
#     member_home = family_soup.find('strong', string=re.compile("Home Phone"))
#     if member_home:
#         return member_home.find_parent().select_one('a[href^="tel:"]').text.strip()
#     return None


# def get_cell_phone(family_soup, name, family):
#     if family is True:
#         family_member_cell = family_soup.find('h3', string=re.compile(name)).find_parent().select_one('a[href^="tel:"]')
#         return family_member_cell.text.strip() if family_member_cell else None
#     else:
#         single_member_cell = family_soup.find('div', attrs={"class": "tc dir"}).find('a', string=re.compile(r"((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}"))
#         return single_member_cell.text.strip() if single_member_cell else None
#     return None


# def get_church_member_phone(first_name, last_name):
#     global __FAMILY_URL
#     login_congregate()
#     # split_names(name)
#     first_name = first_name.capitalize()
#     last_name = last_name.capitalize() if last_name else None
#     church_member_query_result = find_church_member_page(first_name, last_name)
#     if not church_member_query_result:
#         return None
#     __FAMILY_URL += church_member_query_result
#     result = session_requests.get(
#         __FAMILY_URL,
#         headers=dict(referer=__DIRECTORY_URL)
#     )
#     family_soup = BeautifulSoup(result.content, 'html.parser')
#     family = True if family_soup.ul else False
#     home_phone = get_home_phone(family_soup)
#     cell_phone = get_cell_phone(family_soup, first_name, family)
#     phone_numbers = {
#         "Cell": cell_phone,
#         "Home": home_phone
#     }
#     return phone_numbers
