"""
黑马程序员 信息抓取
'''
因为所有的分类都是一套代码 我们只需要修改三处代码即可适配所有的分类课程
1. 翻页页数
2. 课程分类标签
3. 拼接链接
这三处我都有详细代码 配合文档应该还是很好理解的
'''
# 实现翻页 java 有5页内容 从1开始到5 所有range(1,6)
# python 就一页 range(1,2)即可
# c\c++ 两页 range(1,3)即可
# 网络安全 一页 range(1,2)
信息抓取大类
- JAVA
- C\C++\C#
- Python
- 网络安全（信息安全）

具体抓取信息
- 课程封面 1
- 课程名 1
- 主讲人（老师）
- 累计参与课程人数 1
- 评分（或者星级） 1
- 课程链接 1
- 评论数 1

"""
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
    headers={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-HK,zh;q=0.9,zh-CN;q=0.8,en;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'isclose=1; isclose=1; PHPSESSID=gvsqti4dj4aatv35uec0utp672; UM_distinctid=170ee67bba314-0772b9de2c2633-7711a3e-1fa400-170ee67bba451b; href=http%3A%2F%2Fyun.itheima.com%2Fcourse.html; accessId=994d4130-1df9-11e9-b7ec-7766c2691ec6; bad_id994d4130-1df9-11e9-b7ec-7766c2691ec6=caa1e3f1-6932-11ea-86ec-5d3b2603a5c7; nice_id994d4130-1df9-11e9-b7ec-7766c2691ec6=caa1e3f2-6932-11ea-86ec-5d3b2603a5c7; isclose=1; CNZZDATA1261487506=1428183896-1584543386-%7C1584611660; qimo_seosource_994d4130-1df9-11e9-b7ec-7766c2691ec6=%E7%AB%99%E5%86%85; qimo_seokeywords_994d4130-1df9-11e9-b7ec-7766c2691ec6=; pageViewNum=15',
        'Host':'yun.itheima.com',
        'Referer':'http://yun.itheima.com/course/c26/p/4.html?jingjiaczpz-PC-1',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    # 请求传入的网址 这里需要添加请求头部 避免被网站反爬
    con = requests.get(url=url,headers=headers)
    # 避免转码不正确
    con.encoding = con.apparent_encoding
    # 将con转换成可以用Bs4库解析的数据类型 注意con的请求返回的数据需要在后面添加 text 否则无法解析
    soup = BeautifulSoup(con.text,'lxml')
    return soup

# 主体函数 分析定位具体信息并进行提取 然后调用数据库函数 存入数据库中
def get_course_info_list():
    '''
    因为所有的分类都是一套代码 我们只需要修改三处代码即可适配所有的分类课程
    1. 翻页页数
    2. 课程分类标签
    3. 拼接链接
    这三处我都有详细代码 配合文档应该还是很好理解的
    '''
    # 实现翻页 java 有5页内容 从1开始到5 所有range(1,6)
    # python 就一页 range(1,2)即可
    # c\c++ 两页 range(1,3)即可
    # 网络安全 一页 range(1,2)
    for i in range(1,2):
        # java 链接拼接方法url ='http://yun.itheima.com/course/c26/p/{}.html?jingjiaczpz-PC-1'.format(i) # 填充翻页数字进入链接
        # url = 'http://yun.itheima.com/course/c26/p/{}.html?jingjiaczpz-PC-1'.format(i)  # 填充翻页数字进入链接

        # python 列表链接
        # url='http://yun.itheima.com/course/c27.html?jingjiaczpz-PC-1'

        # c\c++
        # url='http://yun.itheima.com/course/c55/p/{}.html?jingjiaczpz-PC-1'.format(i)

        # 网络安全
        url='http://yun.itheima.com/course/c146.html?jingjiaczpz-PC-1'
        # 调用请求HTML页面的函数 返回使用bs4解析后的soup页面
        soup = get_html(url)
        # 定位链接所载位置 提取我们所需要的信息
        div_all_li = soup.find('div', class_='main')
        lis = div_all_li.find('ul').find_all('li')
        # 遍历定位到的li标签 提取里面的 课程图片、名字、链接、学习人数、评分
        for li in lis:
            # 因为黑马没有课程的教师名 为了与别的区分开来 所以做了一个定义
            teacher='黑马程序员'

            # 给定一个技术方向列  避免后续可视化的时候需要调用四个表 直接使用一个表 然后存储三大平台的各个方向的数据
            # 需要修改的地方3 分类分别有 java python c\c++\c# 网络安全
            Technical_direction ='网络安全'

            # 提取课程链接 拼接成可以访问的课程链接
            # 注意 get()方法的写法 提取的就是标签内的属性值 下同
            course_url = 'http://yun.itheima.com/' + li.find('a').get('href')

            # 评论在课程页面 所以还要请求课程的页面 获取评论数
            commits_soup = get_html(course_url)
            commits_nums = commits_soup.find('div',class_='con_fr').find('p',class_='p1').text.replace('人已评分','') # 评论数

            # 提取课程图片 拼接成可以访问的链接方便后续保存
            img_url = 'http://yun.itheima.com/' + li.find('img', class_='mask_img1').get('src')

            # 注意转换称为文本形式
            course_name = li.find('h2').text  # 课程名字

            # 定位方法上同 我们只保存数字 替换掉无关字段
            learned_nums = li.find('div', class_='btm').find('p').text.replace('人学习', '')  # 学习人数

            # 评分
            score = li.find('div', class_='btm').find('span', class_='span2').text
            print(course_url)
            print(teacher)
            print(Technical_direction)
            print(img_url)
            print(course_name)
            print(learned_nums)
            print(score)
            print(commits_nums)
            print('-------------------')
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
                pymysql.escape_string(teacher),
                pymysql.escape_string(Technical_direction),
            )
            # print(sql_2)
            cursor.execute(sql_1)  # 执行命令
            db.commit()  # 提交事务

if __name__ == '__main__':
    # 从首页获取所有课程的信息并存入到数据库
    get_course_info_list()