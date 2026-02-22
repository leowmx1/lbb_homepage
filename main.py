from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from time import *
import requests
import bs4
import yagmail
import re
import html
import bs4
import json
import podcast_data


yag = yagmail.SMTP(user="leowmx_server@163.com",
                   password="XLFANPKHRWETMCLW", host='smtp.163.com')

app = Flask(__name__)
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


@app.route('/podcast')
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


@app.route('/courses')
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


@app.route('/human-design')
def jietu():
    return render_template('解图.html')
