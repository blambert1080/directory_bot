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
    address = get_address(soup)
    anniversary = get_family_date(soup, "Anniversary")
    home_phone = get_home_phone(soup)
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
    address = get_address(soup)
    email = strip_tag(soup.select_one(EMAIL_QUERY))
    cell_phone = get_single_cell_phone(soup)
    home_phone = get_home_phone(soup)
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


def get_address(soup):
    address_tag = soup.find('strong', string=re.compile("Address"))
    address = (None if not address_tag
               else strip_tag(address_tag.find_next_sibling('a')))
    address = address.replace('\n\t\t\t\t', ' ').replace('\n\t\t', ' ')
    maps_link = address_tag.find_next_sibling('a')['href']
    return (None if not address_tag
            else "{0}\n{1}".format(address, maps_link))


def get_home_phone(soup):
    home_phone_tag = soup.find('strong', string=re.compile("Home"))
    return (None if not home_phone_tag
            else strip_tag(home_phone_tag.find_parent('p').select_one('p a')))


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
