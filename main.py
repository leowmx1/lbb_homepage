from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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
import json
import podcast_data


yag = yagmail.SMTP(user="leowmx_server@163.com",
                   password="XLFANPKHRWETMCLW", host='smtp.163.com')

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
    return redirect("//www.leibeibei.cn")


@app.route('/login', methods=["get", "post"])
def login():
    return redirect("//www.leibeibei.cn")


@app.route('/del_user')
def del_user():
    return redirect("//www.leibeibei.cn")


@app.route('/logout')
def logout():
    return redirect("//www.leibeibei.cn")


@app.route('/反馈', methods=["post"])
def feedback():
    return redirect("//www.leibeibei.cn")


@app.route('/人类图咨询须知')
def jietu():
    return render_template('解图.html')


@app.route('/评论', methods=["post"])
def message():
    return redirect("//www.leibeibei.cn/人类图咨询须知")


@app.route('/删除评论')
def dmessage():
    return redirect("//www.leibeibei.cn/人类图咨询须知")


@app.route('/回复', methods=["post"])
def rmessage():
    return redirect("//www.leibeibei.cn/人类图咨询须知")


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
    return make_response({"content": []}, 200)
        
@app.route('/api/register_user')
def register_user():
    return make_response({"content": "数据库功能已移除"}, 200)
        
@app.route('/api/save_code',methods=["post","get"])
def save_code():
    return make_response({"content": "数据库功能已移除"}, 200)


@app.route('/404')
def missing():
    return render_template('missing.html')


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
