# coding=utf-8
import requests
from funcs import *
from config import *
import cPickle as pickle
import os
import logging


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


def get_dept_ids(session):
    """ 获取学院id """
    resp = session.get("http://jwxk.ucas.ac.cn/courseManage/main")
    soup = BeautifulSoup(resp.content, 'html.parser')
    # 获取学院id
    categories = dict([(label.contents[0][:2], label['for'][3:])
                       for label in soup.find_all('label')[2:]])
    dept_ids = []
    for key, val in categories.items():
        # print key, val
        dept_ids.append(val)
    return dept_ids


def get_course_dict(session, identity, dept_ids):
    """ 获取课程id对应 """
    course_dict = {}
    for dept_id in dept_ids:
        form_data = {
            "deptIds": dept_id,
            "sb": 0
        }
        resp = session.post("http://jwxk.ucas.ac.cn/courseManage/selectCourse?s=" + identity, data=form_data)

        soup = BeautifulSoup(resp.text, 'html.parser')
        tbody = soup.body.form.table.tbody
        if tbody:
            tbody = tbody.find_all('tr')
        else:
            return False, "Course Selection is unreachable or not started."
        tmp_dict = dict([(c.span.contents[0], c.span['id'].split('_')[1])
                         for c in tbody])
        # print dept_id
        for k, v in tmp_dict.items():
            course_dict[k] = {
                "id": v,
                "dept_id": dept_id
            }
            # print "\t", k, course_dict[k]
    return course_dict


def choose_course(session, course_dict, identity, course_ids):
    """ 循环选课 """
    print "-------------"
    success_courses = []
    while True:
        for course_id in course_ids:
            if (course_id in course_dict) and (course_id not in success_courses):
                course = course_dict[course_id]
                print "---------------------"
                print course_id, ",", course
                form_data = {
                    'deptIds': course["dept_id"],
                    'sids': course["id"]
                }
                resp = session.post("http://jwxk.ucas.ac.cn/courseManage/saveCourse?s=" + identity, data=form_data)
                msg = get_message(resp.text).strip()
                print msg
                if u"成功" in msg:  # 选课成功,就记录一下,然后保存到ucas_cc.log中
                    success_courses.append(course_id)
                    logging.info(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='ucas_cc.log',
                        filemode='w')

    session = requests.session()
    login(session)
    identity = get_identity(session)                            # 获取身份id

    # 加载course_dict
    course_dict = []
    if os.path.exists("./course_dict.pickle"):
        with open("./course_dict.pickle", "rb") as f:
            course_dict = pickle.load(f)
    else:
        dept_ids = get_dept_ids(session)                            # 获取学院id
        course_dict = get_course_dict(session, identity, dept_ids)  # 获取课程字典, 比较耗时间, 所以做一下缓存
        with open("./course_dict.pickle", "wb") as f:
            pickle.dump(course_dict, f)
            print "saving"

    # 循环慢慢跑把
    choose_course(session, course_dict, identity, course_ids)   # 选课

