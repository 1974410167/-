import random
import json
import threading
from datetime import datetime
from util import util_1
from email_1 import send_email
from threading import Event
import time

user_agent_list = [
"Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
"Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)",
"Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN",
"Mozilla/5.0 (iPhone 6s; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.3.0 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B100 Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
"Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baidubrowser/7.18.21.0 (Baidu; P1 6.0.1)",
"Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.10 (Baidu; P1 6.0.1)",
"Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; vivo Y85 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.6.976 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1",
"Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.2.2",
"Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 UWS/2.12.1.18 Mobile Safari/537.36 AliApp(TB/7.5.4) UCBS/2.11.1.1 WindVane/8.3.0 720X1280",
"Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)",
]

headers = {
    "User-Agent":random.choice(user_agent_list),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": 'close'
}

email_dict = {"78630888":"1047537127@qq.com",'78630822':'1974410167@qq.com'}

def is_true_time():
    l = time.localtime(time.time()).tm_hour
    if l >= 8 or l <= 22:
        return True

class control_thread():

    def __init__(self,ins):
        self.running = True
        self.ins = ins
    def terminate(self):
        self.running = False

    def main(self,courseid,classid,uid,name,teacherfactor):

        signed = []
        while self.running:

            # 如果不在对的时间，终止线程
            if not is_true_time():
                self.terminate()

            # 当signed达到1000，清空，访问占用内存过大
            if len(signed)>=1000:
                signed = []

            # 程序随机睡5-20秒，防止访问过快
            m = random.randint(5, 20)
            time.sleep(m)
            if courseid and classid:
                print(f'{name}--{teacherfactor}--{datetime.now()}--{m}')
                active_list = self.ins.taskactivatelist(courseid, classid, uid)
                if active_list:
                    if active_list[0] not in signed:
                        signed.append(active_list[0])
                        # 查询到活动任务后，等待15秒再签到，防止过快签到，被老师察觉
                        time.sleep(15)
                        TT = self.ins.sign(active_list.pop(0), uid,name)
                        if TT == True:
                            to_address = email_dict[uid]
                            send_email(to_address,name)
                            print("success sign!")
                    else:
                        continue

def main_1():

    with open("cookies.txt", 'r') as f:
        cookies = f.readlines()

    for cookie in cookies:
        cookie = eval(cookie)

        ins = util_1()
        ins.cookies = cookie
        ins.headers = headers

        source_list = ins.get_mycourse_list()
        uid = ins.get_uid()

        for item in source_list:
            courseid = item.get("courseid")
            classid = item.get('classid')
            name = item.get("name")
            teacherfactor = item.get("teacherfactor")

            c_t = control_thread(ins)
            t = threading.Thread(target=c_t.main,args=(courseid,classid,uid,name,teacherfactor))
            t.start()


if __name__ == "__main__":

    is_running = False

    while True:

        # 如果程序在可以运行的时间没有运行，那么运行程序，并把运行标志设置为True
        if not is_running and is_true_time():
            main_1()
            is_running = True

        # 如果程序不在可以运行的时间，那么明显线程已经中断，把is_running设置为False
        if not is_true_time():
            is_running = False

        time.sleep(30)







