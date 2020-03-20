"""
@desc:
@author:afrunk
@software:Pycharm on 2020/3/20
中国大学MOOC课程信息爬虫 交付代码

需要修改2处代码 修改当前要抓取得关键词、修改当前存入数据库的类目名

1.1 信息抓取大类
- JAVA
- C\C++\C#
- Python
- 网络安全（信息安全）

1.2 具体抓取信息
- 课程封面 1
- 课程名 1
- 主讲人（老师）1
- 累计参与课程人数 1
- 评分（或者星级）
- 课程链接 1
- 评论数
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
                     db='bishe',
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

        # 爬取关键词类别
        # ['java', 'python', 'c\c++\c#', '网络安全']
        # 修改处1 修改当前要抓取得类目关键词即可 比如c 或 c++ 或 c#
        leibie_list=['c++']

        # 将关键词转换成URL编码 否则会显示无结果
        def quote(x):
            return urllib.parse.quote(x)
        keywords = list(map(quote, leibie_list))
        # 遍历关键词类别
        for search,leibie in zip(keywords,leibie_list):
            # 分类
            # 需要修改处2 修改当前得分类大类目
            Technical_direction ='c\c++\c#'
            # 翻页
            for y in range(1,9):
                try:
                    self.driver.switch_to.window(search_window)
                except:
                    pass
                #拼接搜索链接
                url='http://www.icourse163.org/search.htm?search={}#/'.format(search)
                self.driver.get(url)

                # 获取当前窗口句柄
                search_window = self.driver.current_window_handle
                # 每页有20个课程 最后一页的数量可能会少于20
                for x in range(1,21):
                    data = []
                    # try:
                    # print("能匹配到关键词 继续下一步\n ")
                    self.driver.switch_to.window(search_window)

                    # 看看是否可以匹配到class为"lists"的模块可以即没有被反扒
                    try:
                        # 匹配到既可以进行下一步的定位元素

                        xpath_div_start = self.driver.find_element_by_class_name("lists").text
                    except:
                        print('无法匹配到开始Div')
                        hint = input("请查看到底哪里出了问题！")

                    # 课程链接
                    try:
                        course_url = self.driver.find_element_by_xpath(
                            '//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"][' + str(
                                x) + ']/div[2]/div/div/div[1]/a').get_attribute('href')
                    except:
                        print('无法提取到当前课程的课程链接')

                    # 图片链接
                    try:
                        # 使用xpath来匹配定位元素的位置 具体的匹配语法是 搜索所有的class='u-img f-fl' '//div[@class="u-img f-fl"]['+str(x)+']'然后在后面的[]中填充我们要抓取的是第几个课程的
                        # 通过遍历即可得到我们所需要的某一个位置的课程信息 如果是超链接则需要添加 get_attribute('属性') 以便提取属性
                        # 学习资料 https://www.cnblogs.com/hustar0102/p/5965095.html
                        img_url = self.driver.find_element_by_xpath('//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"]['+str(x)+']/div[1]/div/img').get_attribute('src')

                    except:
                        print('无法提取到当前课程的封面')

                    # 课程名称
                    try:
                        course_name = self.driver.find_element_by_xpath(
                            '//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"][' + str(
                                x) + ']/div[2]/div/div/div[1]/a/span').text
                    except:
                        print('无法提取到当前课程的课程名')
                        break

                    # 老师名字
                    try:
                        teacher_name = self.driver.find_element_by_xpath(
                            '//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"][' + str(
                                x) + ']/div[2]/div/div/div[2]/a[2]').text
                    except:
                        print('无法提取到当前课程的教师名')

                    # 参与人数
                    try:
                        learned_nums = self.driver.find_element_by_xpath(
                            '//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"][' + str(
                                x) + ']/div[2]/div/div/div[3]/span[2]').text.replace('人参与','')
                    except:
                        print('无法提取到当前课程的参与人数')

                    # 详情页
                    # 课程评分
                    # 详情页
                    try:
                        # 休眠1-4s
                        time.sleep(random.randint(1, 4))
                        # 定位各个详情页的入口
                        xpath_dingwei = '//div[@class="u-clist f-bgw f-cb f-pr j-href ga-click"][' + str(
                                x) + ']/div[2]/div/div/div[1]/a'
                        WebDriverWait(self.driver, 1, 0.5).until(
                            EC.presence_of_element_located((By.XPATH, xpath_dingwei)))
                        continue1 = self.driver.find_element_by_xpath(xpath_dingwei)
                        # 点击该入口
                        continue1.click()
                        # 随机休眠2-4s 否则无法读取评论数和评分
                        time.sleep(random.randint(2,4))

                        # 获取所有的标签页
                        all_window = self.driver.window_handles
                        # 遍历标签页
                        for handle in all_window:
                            # 判断是否属于之前的列表入口页
                            if handle != search_window:
                                # 切换到该详情页
                                self.driver.switch_to.window(handle)

                                # 定位评论的位置 点击后才可查看到我们的评论分和评论数
                                # 使用之前的方法有被遮挡 所以改用了该链接下的方法 进行点击 https://blog.csdn.net/WanYu_Lss/article/details/84137519
                                element = self.driver.find_element_by_xpath('//div[@id="review-tag-button"]')
                                self.driver.execute_script("arguments[0].click();", element)
                                time.sleep(5)

                                # 评分
                                try:

                                    score = self.driver.find_element_by_xpath(
                                        '//*[@id="comment-section"]/div/div[1]/div[1]/span').text

                                except:
                                    score = ""

                                # # 评论数
                                try:
                                    commits_nums = self.driver.find_element_by_xpath(
                                        '//span[@id="review-tag-num"]').text.replace('(', '').replace(')', '')
                                except:
                                    commits_nums = ""
                                self.driver.close()  # 关闭当前标识的窗口
                    except:
                        score = ""
                        commits_nums = ""

                    print('课程链接：' + course_url)
                    print("课程方向：" + Technical_direction)
                    print("课程图片：" + img_url)
                    print("课程名称：" + course_name)
                    print("学习人数：" + learned_nums)
                    print("教师名字：" + teacher_name)
                    print("课程评分：" + score)
                    print("课程评论数：" + commits_nums)
                    print('-------------------')

                    # 使用pymysql.escape_string()函数是为了避免有别的字符串导致入库报错 但是如果是数字的话即不需要使用
                    sql_1 = """
                    INSERT IGNORE INTO courseinfo (course_url,commitsnums,imgurl,coursename,learnednums,score,teacher,technicaldirection)VALUES('{}','{}','{}','{}','{}','{}','{}','{}' )
                    """ \
                        .format(
                        pymysql.escape_string(course_url),
                        pymysql.escape_string(commits_nums),
                        pymysql.escape_string(img_url),
                        pymysql.escape_string(course_name),
                        pymysql.escape_string(learned_nums),
                        pymysql.escape_string(score),
                        pymysql.escape_string(teacher_name),
                        pymysql.escape_string(Technical_direction),
                    )
                    # print(sql_1)
                    cursor.execute(sql_1)  # 执行命令
                    db.commit()  # 提交事务
                    # except:
                    #     pass
                # 将句柄转回搜索页
                try:
                    self.driver.switch_to.window(search_window)
                except:
                    pass
                # 随机等待3-5s给予加载页面的时间
                time.sleep(random.randint(3, 5))
                # 在所有的课程信息都提取到之后添加一个翻页效果
                try:
                    pages = self.driver.find_element_by_link_text("下一页")
                    self.driver.execute_script("arguments[0].click();", pages)
                except:
                    print("当前已经是最后一页！")


if __name__ == '__main__':
    # 爬虫
    Mooc().get_url()