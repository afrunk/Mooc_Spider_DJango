"""
慕课网

'''
    因为所有的分类都是一套代码 我们只需要修改三处代码即可适配所有的分类课程
    1. 翻页页数
    2. 课程分类标签 入库内容
    3. 拼接链接
    这三处我都有详细代码 配合文档应该还是很好理解的
'''

信息抓取大类
- JAVA
- C\C++\C#
- Python
- 网络安全（信息安全）

具体抓取信息
- 课程封面
- 课程名 1
- 主讲人（老师）
- 累计参与课程人数
- 评分（或者星级）
- 课程链接
- 评论数
"""
import time
import random
import  requests
from bs4 import BeautifulSoup
# 链接数据库 必须要 安装 pymysql 库
import pymysql
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='root', # 账号
                     password='password', # 密码
                     db='bishe', # 数据库
                     charset='utf8')
cursor = db.cursor()

# 获取HTML 通过 Bs4处理后返回处理后的结构
def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-HK,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'zg_did=%7B%22did%22%3A%20%2217072359a54680-03a4f1f6e030dc-7711a3e-1fa400-17072359a552bd%22%7D; imooc_uuid=d00527c3-185b-4c56-9768-c70b61b14321; imooc_isnew_ct=1582464064; imooc_isnew=2; redrainTime=2020-2-28; Hm_lvt_f0cfcccd7b1393990c78efdeebff3968=1582464081,1582820084,1582820732; UM_distinctid=170af4b44e5390-0eab54808fc0be-7711a3e-1fa400-170af4b44e8160; mc_channel=imoocsearch; mc_marking=fa7ecda0f32bfd195425ffe086241923; cninfo=imoocsearch-fa7ecda0f32bfd195425ffe086241923; IMCDNS=0; zg_f375fe2f71e542a4b890d9a620f9fb32=%7B%22sid%22%3A%201584545322748%2C%22updated%22%3A%201584547182855%2C%22info%22%3A%201584348052877%2C%22superProperty%22%3A%20%22%7B%5C%22%E5%BA%94%E7%94%A8%E5%90%8D%E7%A7%B0%5C%22%3A%20%5C%22%E6%85%95%E8%AF%BE%E7%BD%91%E6%95%B0%E6%8D%AE%E7%BB%9F%E8%AE%A1%5C%22%2C%5C%22Platform%5C%22%3A%20%5C%22web%5C%22%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.imooc.com%22%2C%22zs%22%3A%200%2C%22sc%22%3A%200%2C%22firstScreen%22%3A%201584545322748%7D; Hm_lpvt_f0cfcccd7b1393990c78efdeebff3968=1584547183; cvde=5e527c404c01f-24',
        'Host': 'www.imooc.com',
        'Referer': 'https://www.imooc.com/search/?type=course&words=Python',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    }
    # 请求传入的网址 这里需要添加请求头部 避免被网站反爬
    con = requests.get(url=url,headers=headers)
    # 将con转换成可以用Bs4库解析的数据类型 注意con的请求返回的数据需要在后面添加 text 否则无法解析
    soup = BeautifulSoup(con.text,'lxml')
    # print(soup)
    return soup

# 主体函数 分析定位具体信息并进行提取 然后调用数据库函数 存入数据库中
def get_course_info_list():
    '''
        因为所有的分类都是一套代码 我们只需要修改三处代码即可适配所有的分类课程
        1. 翻页页数
        2. 课程分类标签 入库内容
        3. 拼接链接
        这三处我都有详细代码 配合文档应该还是很好理解的
    '''
    # java 五页 range(1,6)
    # python 2页 range(1,3)
    # c\c++\c# 都只1页 range(1,2)
    # aqtest 安全测试 只1页 range(1,2)
    for i in range(1,2):
        # c=java  c=python c=c c=cplusplus c=csharp c=aqtest列表入口链接
        url='https://www.imooc.com/course/list?c=aqtest'
        # 调用请求HTML页面的函数 返回使用bs4解析后的soup页面
        soup = get_html(url)
        # 定位链接所载位置 提取我们所需要的信息
        all_div = soup.find('div', class_='moco-course-list').find('div',class_='clearfix')
        divs = all_div.find_all('div',class_='course-card-container')
        # 遍历定位到的div标签 提取里面的 课程图片、名字、链接、学习人数、评分
        for div in divs:
            # 首先要判断是否是免费的如果是画继续抓取 如果不是跳过
            price = div.find('div',class_='price-box').find('span').text
            if price=='免费':
                # 给定一个技术方向列  避免后续可视化的时候需要调用四个表 直接使用一个表 然后存储三大平台的各个方向的数据
                # 需要修改的地方3 分类分别有 java python c\c++\c# 网络安全
                Technical_direction ='网络安全'

                # 提取课程链接 拼接成可以访问的课程链接
                # 注意 get()方法的写法 提取的就是标签内的属性值 下同
                course_url = 'https://www.imooc.com' + div.find('a',class_='course-card').get('href')

                # 提取课程图片 拼接成可以访问的链接方便后续保存
                img_url ='https://'+div.find('img', class_='course-banner lazy').get('data-original')[2:] #

                # 注意转换称为文本形式
                course_name = div.find('h3',class_='course-card-name').text  # 课程名字

                # 定位方法上同 我们只保存数字 替换掉无关字段
                learned_nums = div.find('div', class_='course-card-info').find_all('span')[1].text.replace('"', '')  # 学习人数

                # 评论数、教师名字、评分都在课程页面 所以还要请求课程的页面 获取这三个信息
                commits_soup = get_html(course_url)
                # 详情页的评论有的时候是抓不到的 所以添加 try-except 来提高程序的鲁棒性 避免因为一个小小的报错而停止运行
                try:
                    # 教师名字
                    teacher = commits_soup.find('span',class_='tit').find('a').text
                    # 评分 因为慕课的评分是10分制 所以为了进行归一化 直接除2 全部5分制
                    score = float(commits_soup.find('div', class_='static-item l score-btn').find('span', class_='meta-value').text)/2
                    # 用户评论数
                    commits_nums = commits_soup.find('ul',class_='course-menu').find_all('li')[3].find('span').text
                except:
                    print("该链接的详情页抓取不到信息 ：{}".format(course_url))
                    # print(commits_soup)
                    commits_nums ='0'

                print('课程链接：'+course_url)
                print("课程方向："+Technical_direction)
                print("课程图片："+img_url)
                print("课程名称："+course_name)
                print("学习人数："+learned_nums)
                print("教师名字："+teacher)
                print("课程评分："+str(score))
                print("课程评论数："+commits_nums)
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
                    score,
                    pymysql.escape_string(teacher),
                    pymysql.escape_string(Technical_direction),
                )
                # print(sql_2)
                cursor.execute(sql_1)  # 执行命令
                db.commit()  # 提交事务
            else:
                print("该课程不免费，跳过抓取")
        # 每次翻页的时候随机休眠1-5s
        time.sleep(random.randint(1,5))

if __name__ == '__main__':
    # 从分类列表页获取所有课程的信息并存入到数据库
    get_course_info_list()