# coding=utf-8
""" 快速选课 """
import requests
from funcs import *
from config import *
import logging
from requests.exceptions import ReadTimeout, ConnectTimeout


def get_identity(session):
    """ 获取id """
    # 中间跳转
    resp = session.get("http://sep.ucas.ac.cn/portal/site/226/821", headers=headers)
    identity = resp.text.split('Identity=')[1].split('"'[0])[0]
    session.get(("http://jwxk.ucas.ac.cn/login?Identity=" + identity))
    session.get("http://jwxk.ucas.ac.cn/courseManage/selectedCourse")
    resp = session.get("http://jwxk.ucas.ac.cn/courseManage/main")

    soup = BeautifulSoup(resp.content, 'html.parser')
    # new identify
    identity = soup.form['action'].split('=')[1]
    return identity


def fast_choose_course(session, identity, english_courses):
    """ 快速选课 """
    while True:
        try:
            resp = session.post("http://jwxk.ucas.ac.cn/courseManage/saveCourse?s=" + identity,
                                data=english_courses, timeout=1)
            msg = get_message(resp.text).strip()
            print msg
            if u"成功" in msg:
                exit()
        except ReadTimeout as ex:
            print ex.message
        except ConnectTimeout as ex:
            print ex.message


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='ucas_cc.log',
                        filemode='w')
    while True:  # 循环慢慢跑把
        try:
            session = requests.session()
            if not login(session):
                print "登陆失败"
                exit(-1)
            identity = get_identity(session)                            # 获取身份id
            fast_choose_course(session, identity, des_form)   # 选课
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            print ex.message

