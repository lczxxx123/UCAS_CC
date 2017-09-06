from config import *


def login(session):
    login_url = "http://sep.ucas.ac.cn/slogin"
    form = {
        'userName': username,
        'pwd': password,
        'sb': 'sb',
        'rememberMe': '1'
    }
    session.post(login_url, data=form, headers=headers)
    print session.cookies.get_dict()
    if 'sepuser' in session.cookies.get_dict():
        return True
    return False


def try_choose_chourse(session, course_id):
    add_course_url = "http://sep.ucas.ac.cn/courseManage/addCourseSite.json?courseId=%s" % course_id
    print add_course_url
    resp = session.get(add_course_url)
    print resp.content

