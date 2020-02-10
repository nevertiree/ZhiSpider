# -*- coding: utf-8 -*-

from lxml import etree
from lxml.etree import tostring

MIN_QUESTION_NUM = 10
MIN_THUMB_UP_NUM = 100


class QuestionParser:

    question_name_xpath = './h2[@class="ContentItem-title"]/div[@class="QuestionItem-title"]/a/span'
    question_link_xpath = './h2[@class="ContentItem-title"]/div[@class="QuestionItem-title"]/a/@href'
    question_ans_num_xpath = './div[@class="ContentItem-actions"]/' \
                             'a[@class="Button ContentItem-action Button--plain"]/text()'

    def parse(self, element_list: list):  # 输入进行过解析的HTML

        result_list = []

        for elem in element_list:

            try:
                # 获得问题名字
                name = tostring(elem.xpath(self.question_name_xpath)[0], encoding="unicode")
                name = name.replace('<span class="Highlight">', "")
                name = name.replace('</span>', "")
                name = name.replace('<em>', "")
                name = name.replace('</em>', "")

                # 获得问题链接
                link = "https://www.zhihu.com" + elem.xpath(self.question_link_xpath)[0]

                # 获得问题下的回答个数
                num = elem.xpath(self.question_ans_num_xpath)[0]
                num = num.replace("个回答", "")
                num = int(num)

                if num > MIN_QUESTION_NUM:
                    result_list.append({"name": name, "link": link, "num": num})

            except IndexError as e:
                print(e)

        return result_list


class AnswerParser:

    ans_name_xpath = './h2[@class="ContentItem-title"]/div[@itemprop="zhihu:question"]/meta[@itemprop="name"]/@content'
    ans_link_xpath = './h2[@class="ContentItem-title"]/div[@itemprop="zhihu:question"]/' \
                     'a[@data-za-detail-view-id="3942"]/@href'
    thumbs_up_num_xpath = './div[@class="RichContent Highlight is-collapsed"]/div[@class="ContentItem-actions"]' \
                          '/span/button[@class="Button VoteButton VoteButton--up"]' \
                          '/text()'

    def parse(self, element_list: list):  # 输入进行过解析的HTML

        result_list = []

        for elem in element_list:

            try:
                # 获得回答名字
                name = elem.xpath(self.ans_name_xpath)[0]

                # 获得问题链接
                link = "https://www.zhihu.com" + elem.xpath(self.ans_link_xpath)[0]

                # 获得回答赞数
                num = elem.xpath(self.thumbs_up_num_xpath)[0]
                num = num.replace("赞同", "")
                if num.endswith("K"):
                    num = float(num[:-1]) * 1000
                elif num == "":
                    num = 0
                else:
                    num = int(num)

                result_list.append({"name": name, "link": link, "num": num})
            except IndexError as e:
                print(e)

        return result_list


class PageParser:

    question_xpath = '//div[@class="ContentItem"]'
    answer_xpath = '//div[@class ="ContentItem AnswerItem"]'

    question_parser = QuestionParser()
    answer_parser = AnswerParser()

    def parse(self, element_tree: etree.ElementTree):  # 输入进行过解析的HTML

        # 解析问题
        question_elem_list = element_tree.xpath(self.question_xpath)
        print(len(question_elem_list))
        q_list = self.question_parser.parse(question_elem_list)

        # 解析回答
        answer_elem_list = element_tree.xpath(self.answer_xpath)
        print(len(answer_elem_list))
        a_list = self.answer_parser.parse(answer_elem_list)

        return q_list, a_list


if __name__ == '__main__':

    page = etree.parse(r"html\e2799740e4f3b4944a417740a984f5bc.html", etree.HTMLParser())

    page_parser = PageParser()
    print(page_parser.parse(page))
