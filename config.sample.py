# coding=utf-8

username = ""   # 用户名
password = ""   # 密码

# 要选的课
des_courses = [
    # {
    #     "id": "TYMGX010H-03",
    #     "degree": False   # 是否是学位课
    # },
    {
        "id": "201M5019H",
        "degree": True   # 是否是学位课
    }
]


headers = {
    'Host': 'sep.ucas.ac.cn',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
}
