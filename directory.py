import congregate_session
import re


DATE_RE = r'^[0-9]{2}\/[0-9]{2}'
FULL_NAME_RE = "^(?=.*\\b{0}\\b)(?=.*\\b{1}\\b).*$"
FIRST_NAME_RE = "(?=.*\\b{}).*$"
LAST_NAME_RE = "^(?=.*\\b{}\\b)"
CELL_QUERY = r'a[href^="tel:"]'
EMAIL_QUERY = r'a[href^="mailto:"]'


def get_church_member_page(first_name, last_name):
    # Directory Searching
    directory_soup = congregate_session.get_directory_page_soup()
    if last_name:
        if is_more_than_one_result(directory_soup, last_name, False):
            return get_member_number(
                directory_soup, FULL_NAME_RE.format(last_name, first_name))
        return get_member_number(directory_soup, last_name, False)
    else:
        return (get_all_possible_names(directory_soup, first_name)
                if is_more_than_one_result(directory_soup, first_name, True)
                else get_member_number(directory_soup, first_name, True))


def get_church_member_info(first_name, last_name):
    member_results = get_church_member_page(first_name, last_name)
    matched_member_info = {}
    if type(member_results) is list:
        return member_results
    else:
        return process_results(member_results)
    return matched_member_info


# ************************* HELPER FUNCTIONS ****************************
def process_results(family_link):
    family_soup = (congregate_session
                   .get_church_member_page_soup(family_link))
    if not family_soup:
        return None
    return (process_family_members(family_soup) if family_soup.li
            else process_single_members(family_soup))


def is_more_than_one_result(soup, name, is_first_name):
    name_re = (FIRST_NAME_RE.format(name) if is_first_name
               else LAST_NAME_RE.format(name))
    names = soup.find_all('h3', string=re.compile(name_re, re.IGNORECASE))
    return len(names) > 1


def get_member_number(soup, name, is_first_name):
    name_re = (FIRST_NAME_RE.format(name) if is_first_name
               else LAST_NAME_RE.format(name))
    name_found = soup.find('h3', string=re.compile(name_re, re.IGNORECASE))
    return (None if not name_found else name_found.find_parent('a')['href'])


def get_all_possible_names(soup, name_searched):
    name_re = FIRST_NAME_RE.format(name_searched)
    names = []
    for name in soup.find_all('h3', string=re.compile(name_re, re.IGNORECASE)):
        name = strip_tag(name)
        name_chunks = name.split(', ')
        if name_searched in name_chunks[0].lower():
            last_name = name_chunks[0]
            first_name = name_chunks[1].split(' ')[0]
        else:
            first_name_start = name.split(', ')[1]
            first_name = find_matching_first_name(first_name_start, name_searched)
            last_name = name.split(', ')[0]
        full_name = "{0} {1}".format(first_name, last_name)
        names.append(full_name)
    return names


def process_family_members(soup):
    address = get_address(soup)
    image = get_image(soup)
    home_phone = get_home_phone(soup)
    anniversary = get_family_date(soup, "Anniversary")
    family_members = {}
    for index, member in enumerate(soup.select('li')):
        cell_phone = get_family_cell_phone(member)
        birthday = get_family_date(member, "Birthday")
        anniversary = None if index > 1 else anniversary
        email = strip_tag(member.select_one(EMAIL_QUERY))
        name = strip_tag(member.h3)
        family_members[name] = get_family_info(address, anniversary, birthday,
                                               cell_phone, email, home_phone,
                                               image, name)
    return family_members


def process_single_members(soup):
    address = get_address(soup)
    image = get_image(soup)
    home_phone = get_home_phone(soup)
    cell_phone = get_single_cell_phone(soup)
    email = strip_tag(soup.select_one(EMAIL_QUERY))
    birthday = strip_tag(soup.find('p', string=re.compile(DATE_RE)))
    name = " ".join(strip_tag(soup.body.div.div.h1).split(', ')[::-1])
    single_member = {}
    single_member[name] = get_family_info(address, None, birthday, cell_phone,
                                          email, home_phone, image, name)
    return single_member


def get_address(soup):
    address_tag = soup.find('strong', string=re.compile("Address"))
    if address_tag:
        address = strip_tag(address_tag.find_next_sibling('a'))
        address = address.replace('\n\t\t\t\t', ' ').replace('\n\t\t', ' ')
        maps_link = ("[Google Maps Link]({0})"
                     .format(address_tag.find_next_sibling('a')['href']))
        return "{0}\n{1}".format(address, maps_link)
    return None


def get_family_date(soup, date):
    date_tag = soup.find('dt', string=re.compile(date))
    return (strip_tag(date_tag.find_next_sibling('dd')) if date_tag
            else None)


def get_family_cell_phone(soup):
    return strip_tag(soup.select_one(CELL_QUERY))


def get_home_phone(soup):
    home_phone_tag = soup.find('strong', string=re.compile("Home"))
    return (None if not home_phone_tag
            else strip_tag(home_phone_tag.find_parent('p').select_one('p a')))


def get_image(soup):
    return "{0}{1}".format(congregate_session.__FAMILY_URL,
                           soup.div.div.p.img['src'])


def get_family_info(address, anniversary, birthday, cell_phone,
                    email, home_phone, image, name):
    return {
        "address": address,
        "anniversary": anniversary,
        "birthday": birthday,
        "cell_phone": cell_phone,
        "email": email,
        "home_phone": home_phone,
        "image": image,
        "name": name
    }


def get_single_cell_phone(soup):
    cell_tag = soup.find('h4', string=re.compile("Cell"))
    return (None if not cell_tag
            else strip_tag(cell_tag.find_next_sibling('p').select_one('p a')))


def find_matching_first_name(name_result, name_searched):
    names = re.split(r' & | |\(|\)', name_result)
    return [name for name in names if name_searched in name.lower()][0]


def strip_tag(tag):
    return None if not tag else tag.text.strip()
