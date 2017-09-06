import requests
from funcs import *


if __name__ == "__main__":
    session = requests.session()
    login(session)
    try_choose_chourse(session, "138161")


