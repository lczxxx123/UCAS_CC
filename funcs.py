from config import *
from bs4 import BeautifulSoup


def login(session):
    login_url = "http://sep.ucas.ac.cn/slogin"
    form = {
        'userName': username,
        'pwd': password,
        'sb': 'sb'
    }
    session.post(login_url, data=form, headers=headers)
    print session.cookies.get_dict()
    if 'sepuser' in session.cookies.get_dict():
        return True
    return False


def get_message(html):
    css_soup = BeautifulSoup(html, 'html.parser')
    text = css_soup.select('#main-content > div > div.m-cbox.m-lgray > div.mc-body > div')[0].text
    return "".join(line.strip() for line in text.split('\n'))

