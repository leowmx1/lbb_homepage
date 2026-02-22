from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymysql  
from time import *
import requests
import bs4
import yagmail
import re
import html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import bs4
import ast
import json
import podcast_data


yag = yagmail.SMTP(user="leowmx_server@163.com",
                   password="XLFANPKHRWETMCLW", host='smtp.163.com')

# Disable database connection for testing

db = pymysql.connect(host='localhost',
                     user='root',
                     password='841128',
                     database='Homepage',
                     autocommit=True)
cursor = db.cursor()

sql = '''CREATE TABLE IF NOT EXISTS USER
        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        NAME CHAR(255) NOT NULL,
        PASSWORD CHAR(255) NOT NULL,
        CONTACT CHAR(255) NOT NULL);'''

cursor.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS MESSAGES
        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        NAME CHAR(255) NOT NULL,
        MESSAGE TEXT NOT NULL,
        REPLY TEXT);'''

cursor.execute(sql)

sql = '''CREATE TABLE IF NOT EXISTS CLOUD_SAVE_CODE
        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
        NAME CHAR(255) NOT NULL,
        PASSWORD CHAR(255) NOT NULL,
        CODE TEXT);'''

cursor.execute(sql)



# # Mock cursor and db for testing
# class MockCursor:
#     def execute(self, sql):
#         print(f"Mock executing SQL: {sql}")
#         return True
    
#     def fetchall(self):
#         return []

# class MockDB:
#     def ping(self, reconnect=True):
#         return True

# cursor = MockCursor()
# db = MockDB()

app = Flask(__name__)
app.config["SECRET_KEY"] = "！#%&）*！@#￥%urdtfgdhs^%%&%TYJRYTYUTYUTI{}OPI{YUTTYEYRWET#%$^@^#!!#@$!$@~$!@!#@%$#%$^&%&(*^&(&&*^(ioevsrtyberoytw8eterytuvyrbUSEVRUWTBYOERTYERIOTYERYEVTUWIBYTUERIOTUERBYOTURETYOERBTYURITBYEOTYERIYTOE4857209347590374502738479787877878787878787&*&*&*^($%^$&%&^*&Q#_#}{|}}|}|}|||||||||ryuvtew74br64vreyr eyvowerwuryeoutreuytutyreutuwrtyuwutreuteryutrwtyertyuweryutywerutytyerutwuytuyeturytwuerytureoytuerytoeurytiutyeiutyrtreyutyoeriutyuoyteoityweutriyutyueyturwytoruyuetyioeryt"

@app.route('/', methods=["get", 'post'])

def index():
    # json_data=request.get_json()

    echostr = request.values.get("echostr")
    if echostr == None:
        if session == True:
            return render_template("homepage.html")
        else:
            return render_template("homepage.html")
    else:
        return echostr
        # return


@app.route('/播客')
def xiaoyuzhou():
    # 获取订阅者数量
    head = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"
    }
    url = "https://www.xiaoyuzhoufm.com/podcast/62c522cd42e3d7d26948b47e?s=eyJ1IjoiNjJiM2ExNzdlZGNlNjcxMDRhYzFkNWU2In0%3D"
    res = requests.get(url, headers=head)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    data = soup.find("span", class_="jsx-4bf8abe794d14385 digit")
    subscriber_count = data.text
    
    
    # 按播放量排序
    featured_episodes = podcast_data.get_featured_episodes()
    
    return render_template('播客.html', 
                         sub=subscriber_count,
                         featured_episodes=featured_episodes)


@app.route('/课程')
def class_list():
    head = {
        "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11"
    }
    url = "https://www.xiaoyuzhoufm.com/podcast/62c522cd42e3d7d26948b47e?s=eyJ1IjoiNjJiM2ExNzdlZGNlNjcxMDRhYzFkNWU2In0%3D"
    res = requests.get(url, headers=head)
    soup = bs4.BeautifulSoup(res.text, "lxml")
    data = soup.find("span", class_="jsx-4bf8abe794d14385 digit")
    n = data.text

    return render_template('课程列表.html', subscriptions_num=n)
# @app.route('/人类图解图')
# def solution_graph():
#    return render_template('解图.html')


@app.route('/登录')
def login_page():
    return render_template('login.html')


@app.route('/注册')
def register_page():
    return render_template('register.html')


@app.route('/register', methods=["get", "post"])
def register():
    safe = request.values.get("g-recaptcha-response")
    if safe != "":
        user_name = request.values.get("username")
        pwd = request.values.get("pwd")
        pwd2 = request.values.get("pwd2")
        contact = request.values.get("contact")
        user_list = []
        # after_pwd = ""
        # for i in pwd:
        #    ascii_i = ord(i)
        #    after_i = chr(ascii_i + 3)
        #    after_pwd = after_pwd + after_i
        sql = """SELECT * FROM USER;"""
        db.ping(reconnect=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            USERNAME = row[1]
            user_list.append(USERNAME)
        if pwd != pwd2:
            return render_template('register.html', error="两次输入的密码不相同")
        elif user_name in user_list:
            return render_template('register.html', error="用户名已被注册")
        else:
            after_PASSWORD = ""
            for i in pwd:
                ascii_i = ord(i)
                after_i = chr(ascii_i + 3)
                after_PASSWORD = after_PASSWORD + after_i
            sql = """INSERT INTO USER(
                        NAME,PASSWORD,CONTACT)
                    VALUES ('%s','%s','%s')""" % (user_name, after_PASSWORD, contact)
            print(sql)
            db.ping(reconnect=True)
            cursor.execute(sql)
            session["username"] = user_name
            session.permanent = True
            return redirect("//www.leibeibei.cn")
    else:
        return "<h1 style='color:red' align=center>无效操作，请完成人机验证！</h1>"


@app.route('/login', methods=["get", "post"])
def login():
    safe = request.values.get("g-recaptcha-response")
    if safe != "" or request.values.get("username") == "**//root_admin//**" or request.values.get("username") == "王铭瑄":
        user_name = request.values.get("username")
        pwd = request.values.get("pwd")
        # re = request.values.get("remember")
        user_dict = {}
        # after_pwd = ""
        # for i in pwd:
        #    ascii_i = ord(i)
        #    after_i = chr(ascii_i + 3)
        #    after_pwd = after_pwd + after_i
        sql = """SELECT * FROM USER;"""
        db.ping(reconnect=True)
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            USERNAME = row[1]
            PASSWORD = row[2]
            before_PASSWORD = ""
            for i in PASSWORD:
                ascii_i = ord(i)
                before_i = chr(ascii_i - 3)
                before_PASSWORD = before_PASSWORD + before_i
            user_dict[USERNAME] = before_PASSWORD
        if user_name in user_dict:
            if user_dict[user_name] == pwd:
                session["username"] = user_name
        #       if re == "off":
        #           session.permanent=False
        #           session_parameters['timeout'] = 1
        #      else:
                session.permanent = True
                return redirect("//www.leibeibei.cn")
            else:
                return render_template('login.html', error="用户名或密码错误(1)")
        else:
            return render_template('login.html', error="用户名或密码错误(2)")
    else:
        return "<h1 style='color:red' align=center>无效操作，请完成人机验证！</h1>"


@app.route('/del_user')
def del_user():
    if session["username"]:
        user_name = session["username"]
        sql = """DELETE FROM USER WHERE NAME='%s';""" % (user_name)
        db.ping(reconnect=True)
        cursor.execute(sql)
        del session["username"]
    return redirect("//www.leibeibei.cn")


@app.route('/logout')
def logout():
    if session["username"]:
        del session["username"]
    return redirect("//www.leibeibei.cn")


@app.route('/反馈', methods=["post"])
def feedback():
    user_name = session["username"]
    p_class = request.values.get("class")
    specific = request.values.get("specific")
    check = request.values.get("g-recaptcha-response")
    if check == '':
        sleep(5)
        return "<h1 style='color:red' align=center>反馈无效，请完成人机验证！</h1>"
    sql = """SELECT * FROM USER WHERE NAME='%s';""" % (user_name)
    db.ping(reconnect=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        CONTACT = row[3]
    '''with open("feedback.txt","a") as f:
        text = """\n-----------------------用户反馈----------------------------
        用户名:'%s'
        类型:'%s'
        具体内容:'%s'
        联系方式:'%s'
------------------------------------------------------------\n\n""" % (user_name,p_class,specific,CONTACT)
        f.write(text)'''
    content = "用户名:'%s'\n类型:'%s'\n具体内容:'%s'\n联系方式:'%s'" % (
        user_name, p_class, specific, CONTACT)
    yag.send(
        # to 收件人，如果一个收件人用字符串，多个收件人用列表即可
        to=['leibei1128@163.com'],
        # subject 邮件主题（也称为标题）
        subject='网站用户反馈',
        # contents 邮件正文
        contents=content,
        # attachments 附件，和收件人一致，如果一个附件用字符串，多个附件用列表
        # 记得关掉链接，避免浪费资源\
    )
    yag.close()
    sleep(5)
    return redirect("//www.leibeibei.cn")


@app.route('/人类图咨询须知')
def jietu():
    sql = '''SELECT * FROM MESSAGES''';
    db.ping(reconnect=True)
    cursor.execute(sql)
    res = cursor.fetchall()
    raw_num = 0
    messages = []
    for raw in res:
        raw_num += 1
        print(raw[2])
        s = re.sub(r'\n', '<br>', raw[2])
        try:
            s2 = re.sub(r'\n', '<br>', raw[3])
        except:
            s2 = ""

        messages.append({"id": raw[0], "用户名": raw[1], "留言": s, "老师回复": s2})
    messages.reverse()
    return render_template('解图.html', rawnum=raw_num, messages=messages)


@app.route('/评论', methods=["post"])
def message():
    noname = request.values.get("no_name")
    if noname == None:
        try:
            if session["username"]=="**//root_admin//**":
                user_name = "网站管理员"
            else:
                user_name = session["username"]
        except KeyError:
            user_name = "匿名用户"
    else:
        user_name = "匿名用户"
    message = request.values.get("message")
    sql = """INSERT INTO MESSAGES(
                        NAME,MESSAGE,REPLY)
                    VALUES (\"%s\",\"%s\",NULL)""" % (user_name, message)
    db.ping(reconnect=True)
    cursor.execute(sql)

    return redirect("http://www.leibeibei.cn/人类图咨询须知")


@app.route('/删除评论')
def dmessage():
    id = request.values.get("id")
    sql = """DELETE FROM MESSAGES WHERE ID='%s';""" % (id)
    db.ping(reconnect=True)
    cursor.execute(sql)

    return redirect("http://www.leibeibei.cn/人类图咨询须知")


@app.route('/回复', methods=["post"])
def rmessage():
    id = request.values.get("id")
    rtext = request.values.get("rtext")
    # re.sub('\'',r'\'',rtext)
    sql = """UPDATE MESSAGES SET REPLY = \"%s\" WHERE ID = \"%s\";""" % (
        rtext, id)
    db.ping(reconnect=True)
    cursor.execute(sql)

    return redirect("http://www.leibeibei.cn/人类图咨询须知")


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/test_form', methods=["post"])
def test_form():
    save = request.values.get('g-recaptcha-response')
    if save == '':
        return "<h1 style='color:red' align=center>无效</h1>"

# @app.route('/s')
# def share():
#     return render_template('share.html')


@app.route('/api/get_code')
def api_get_code():
    url = request.values.get("url")
    code = ""
    if url == None:
        return {"status": "404", "error": "url missing"}

    def request_url(url):
        # path =  Service("/root/lbb/chromedriver")
        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        # Specify any available port
        option.add_argument('--remote-debugging-port=9515')
        # Recommended for Docker environments
        option.add_argument('--no-sandbox')
        # Avoid crashes due to limited /dev/shm size
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--disable-gpu')

        browser = webdriver.Chrome(
            executable_path="/root/lbb/chromedriver", options=option)
        browser.get(url)

        sleep(2)

        return browser.page_source.encode("utf-8")

    def parse_html(html):
        soup = bs4.BeautifulSoup(html, 'lxml')
        tags = soup.find_all("div", class_="ace_line")
        code = ""
        for tag in tags:
            code += (tag.text + "\n")
        return code

    def get_code(url):
        return parse_html(request_url(url))
    code = get_code(url)

    response = make_response({"content": code}, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = 'chrome-extension://bjloijnddgglaefdigkgppijkfhoacho'
    # return {"status":"200","content":{"code":code}}
    return response

@app.route('/api/get_UPC')
def get_user():
    sql = """SELECT * FROM CLOUD_SAVE_CODE;"""
    db.ping(reconnect=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    
    response = make_response({"content": results}, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    
    return response
        
@app.route('/api/register_user')
def register_user():
    username = request.values.get("username")
    password = request.values.get("pwd")
    
    sql = """SELECT * FROM CLOUD_SAVE_CODE;"""
    db.ping(reconnect=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        USERNAME=row[1]
        if username == USERNAME:
            response = make_response({"content": "用户名已被注册"}, 200)
            response.headers['Content-Type'] = 'text/plain; charset=utf-8'
            
            return response
    
    sql = """INSERT INTO CLOUD_SAVE_CODE(
                        NAME,PASSWORD,CODE)
                    VALUES ('%s','%s','%s')""" % (username, password, str({}))
    db.ping(reconnect=True)
    cursor.execute(sql)
    
    response = make_response({"content": "用户注册成功"}, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    
    return response
        
@app.route('/api/save_code',methods=["post","get"])
def save_code():
    username = request.values.get("username")
    filename = request.values.get("fn")
    code_text = request.values.get("code")
    
    sql = "SELECT * FROM CLOUD_SAVE_CODE;"
    db.ping(reconnect=True)
    cursor.execute(sql)
    results = cursor.fetchall()
    for raw in results:
        if raw[1]==username:
            print(raw[3],type(raw[3]))
            dict_str=raw[3]
            
            fixed_dict_str = ""
            dict_value=dict_str.split(",")
            if dict_str=="{}":
                code_list={}
            else:
                for i in dict_value:
                    i_list=i.split(":")
                    if i==dict_value[-1]:
                        fixed_dict_str += i_list[0]+':\''+i_list[1][1:-2].replace("\'","\\'").replace('\"','\\"').replace("\n","\\n")+"'}"
                        continue
                    fixed_dict_str += i_list[0]+':\''+i_list[1][1:-1].replace("\'","\\'").replace('\"','\\"').replace("\n","\\n")+'\','
                #print(fixed_dict_str)
                code_list = ast.literal_eval(fixed_dict_str)
   
    code_list[filename]=code_text
    
    sql = 'UPDATE CLOUD_SAVE_CODE SET CODE = "%s" WHERE NAME="%s";' % (str(code_list).replace("\"","\'"),username)
    print(sql)
    db.ping(reconnect=True)
    cursor.execute(sql)
    
    response = make_response({"content": "代码保存成功"}, 200)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    
    return response


@app.route('/404')
def missing():
    return render_template('missing.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
