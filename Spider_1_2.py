"""
@desc:
@author:afrunk
@software:Pycharm on 2020/3/20
获取详情页的评论数和评分 测试代码
"""

import urllib.parse  # 后面将要搜索的关键字转换为url形式会用到
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait                    # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC           # available since 2.26.0
import os
import random
import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root',
                     password='password',
                     db='world',
                     charset='utf8')
cursor = db.cursor()

class Mooc():
    def __init__(self):
        # selenium
        self.Frefiox_options = Options()
        self.driver = webdriver.Firefox()
    def get_url(self,search ='python'):
        """
        获取搜索职位的url, demo里面默认搜索python
        :param search:
        :return:
        """
        #拼接搜索链接
        url='http://www.icourse163.org/course/UESTC-1003040002'
        self.driver.get(url)

        # 定位评论的位置 点击后才可查看到我们的评论分和评论数
        # 使用之前的方法有被遮挡 所以改用了该链接下的方法 进行点击 https://blog.csdn.net/WanYu_Lss/article/details/84137519
        element = self.driver.find_element_by_xpath('//div[@id="review-tag-button"]')
        self.driver.execute_script("arguments[0].click();", element)
        # time.sleep(10)

        # 评分
        try:

            score = self.driver.find_element_by_xpath(
                '//*[@id="comment-section"]/div/div[1]/div[1]/span').text

        except:
            score = ""

        # # 评论数
        try:
            commits_nums = self.driver.find_element_by_xpath(
                '//span[@id="review-tag-num"]').text.replace('(','').replace(')','')
        except:
            commits_nums = ""
        # self.driver.close()  # 关闭当前标识的窗口
        print("课程评分：" + score)
        print("课程评论数：" + commits_nums)
        print('-------------------')

if __name__ == '__main__':
    # 爬虫
    Mooc().get_url()