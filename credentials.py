import os

__username = os.environ['DIR_USERNAME']
__password = os.environ['SECRET_PASS']
__token = os.environ['DIR_BOT_TOKEN']
__url_beginning = os.environ['DIR_BOT_URL']
__LOGIN_URL = __url_beginning + "/mobile/login"
__DIRECTORY_URL = __url_beginning + "/mobile/directory"
__DASHBOARD_URL = __url_beginning + "/mobile/dashboard"
__FAMILY_URL = __url_beginning


login = {
    "username": __username,
    "password": __password,
    "token": __token
}


urls = {
    "login_url": __LOGIN_URL,
    "directory_url": __DIRECTORY_URL,
    "dashboard_url": __DASHBOARD_URL,
    "family_url": __FAMILY_URL
}