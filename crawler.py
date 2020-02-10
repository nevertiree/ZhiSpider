# -*- coding: utf-8 -*-

import os
import time
import json
import hashlib

from selenium import webdriver

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

with open('cookie.txt') as json_file:
    cookie_json = json.load(json_file)


def query_2_hash(query: str):
    return hashlib.md5(query.encode()).hexdigest()


class Crawler:

    def __init__(self):

        self.browser = webdriver.Chrome()
        self.browser.maximize_window()

        self.browser.get('https://zhihu.com')

        for cookie_item in cookie_json:
            cookie_item = {
                'domain': cookie_item["domain"],
                'name': cookie_item['name'],
                'value': cookie_item['value'],
                'path': '/',
                'expires': None
            }
            self.browser.add_cookie(cookie_item)

    def save_page_cache(self, query):

        # 生成URL
        url = f'https://www.zhihu.com/search?type=content&q={query}'
        self.browser.get(url)

        # 拖拽滚动条
        for i in range(10):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # 休眠2秒

        # 获取页面内容
        html_source = self.browser.page_source

        query_hash = query_2_hash(query)
        # 保存到本地
        with open(os.path.join("html", query_hash+".html"), "a+", encoding="utf-8") as f:
            for item in html_source:
                f.write(item)

        # 记录hash对应值
        with open("hash.log", "a+", encoding="utf-8") as f:
            f.write(query + "-" + query_hash)

        return query_hash


if __name__ == '__main__':
    pass
