# coding=utf-8
from paser import *


def scheduling(url):
    worker = PeoplePaser(url)
    if 'people.com.cn/n' in url:
        state = worker.switch_methods('body_paser')
    elif url.endswith('people.com.cn') or 'GB' in url or 'index' in url:
        state = worker.switch_methods('any_url_paser')
    elif url == 'http://www.people.com.cn/':
        state = worker.switch_methods('home_paser')
    else:
        state = 'typeError'
    print(state)


if __name__ == "__main__":
    url = 'http://politics.people.com.cn/n1/2017/0418/c1001-29218992.html'
    # url='http://www.people.com.cn/'
    scheduling(url)
    # home_paser('http://www.people.com.cn/')
    # body_paser('http://politics.people.com.cn/n1/2017/0412/c1001-29205965.html')
