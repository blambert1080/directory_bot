import credentials
import directory
from bs4 import BeautifulSoup


SINGLE_PHOTO = "/media/photos/singlephoto.jpg"
FAMILY_PHOTO = "/media/photos/familyphoto.jpg"
SINGLE_SOUP = BeautifulSoup(open("test_soup/single_family_member.html"),
                            'html.parser')
FAMILY_SOUP = BeautifulSoup(open("test_soup/family_members.html"),
                            'html.parser')


def test_image():
    assert (directory.get_image(SINGLE_SOUP) ==
            "{0}{1}".format(credentials.__FAMILY_URL, SINGLE_PHOTO))
    assert (directory.get_image(FAMILY_SOUP) ==
            "{0}{1}".format(credentials.__FAMILY_URL, FAMILY_PHOTO))


def test_process_single_member_info():
    single_info = directory.process_single_members(SINGLE_SOUP)['Single User']
    address_result = single_info['address']
    address_check = ("123 Main St El Paso, TX 75132\n" +
                     "http://maps.google.com/example_map_reference")
    # Cast address to String
    assert address_result == address_check, (
        ("Addresses are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(address_result, address_check)))
    birthday_result = single_info["birthday"]
    birthday_check = "01/01"
    assert birthday_result == birthday_check, (
        ("Birthdays are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(birthday_result, birthday_check)))
    home_phone_result = single_info["home_phone"]
    home_phone_check = "(972) 123-4567"
    assert home_phone_result == home_phone_check, (
        ("Home Phone Numbers are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(home_phone_result, home_phone_check)))
    cell_phone_result = single_info["cell_phone"]
    cell_phone_check = "(214) 123-4567"
    assert cell_phone_result == cell_phone_check, (
        ("Cell Phone Numbers are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(cell_phone_result, cell_phone_check)))
    email_result = single_info["email"]
    email_check = "email@example.com"
    assert email_result == email_check, (
        ("Emails are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(email_result, email_check)))
    family_photo_result = single_info["image"]
    family_photo_check = (credentials.__FAMILY_URL +
                          "/media/photos/singlephoto.jpg")
    assert family_photo_result == family_photo_check, (
        ("Emails are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(family_photo_result, family_photo_check)))
    name_result = single_info["name"]
    name_check = "Single User"
    assert name_result == name_check, (
        ("Names are not equal\nResult:\n{0}\nCheck:\n{1}\n"
            .format(name_result, name_check)))

