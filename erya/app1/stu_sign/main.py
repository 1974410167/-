import random
import os
import threading
from datetime import datetime
import time
import sys

module_dir = os.path.dirname(__file__)
sys.path.append(module_dir)

import util
import email_1
import redis_1

django_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(django_dir)

print(django_dir)
from models import User


s = User.objects.all()
print(s)


# redis = op_redis()

def get_headers():
    user_agent_list = [
        '(Linux; Android 10; MI 8 SE Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 com.chaoxing.mobile/ChaoXingStudy_3_4.7.4_android_phone_593_53 (@Kalimdor)_a79813a3bf4449a181b0ec96e2446126',
        '(Linux; Android 8.1.0; 16th Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.110 Mobile Safari/537.36 com.chaoxing.mobile/ChaoXingStudy_3_4.7.4_android_phone_593_53 (@Kalimdor)_ff1be61fd8af4151ae15f8d21e61dfbd',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 com.ssreader.ChaoXingStudy/ChaoXingStudy_3_4.7.3_ios_phone_202010231900_53 (@Kalimdor)_8265879478444729073',
    ]

    headers = {
        "User-Agent":random.choice(user_agent_list),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": 'close'
    }
    return headers

def is_true_time():
    l = time.localtime(time.time()).tm_hour
    if l >= 7 and l <= 9:
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
                active_list = self.ins.taskactivatelist(courseid, classid, uid)
                if active_list:
                    if active_list[0] not in signed:
                        signed.append(active_list[0])
                        # 查询到活动任务后，等待15秒再签到，防止过快签到，被老师察觉
                        time.sleep(15)
                        TT = self.ins.sign(active_list.pop(0), uid,name)
                        if TT == True:
                            print("success sign!")
                    else:
                        continue

# def main_1():


        # u = util.util_1()
        # u.cookies = 's'
        # u.headers = get_headers()
        # s = u.get_mycourse_list()
        # if not s:


#
# def update_cookie(uid):
#
#
# main_1()

# if __name__ == "__main__":
#
#     is_running = False
#
#     n = 1
#     while True:
#         # 如果程序在可以运行的时间没有运行，那么运行程序，并把运行标志设置为True
#         if not is_running and is_true_time():
#
#             s = send_email("1974410167@qq.com",'签到系统已启动')
#             s.send()
#             main_1()
#             is_running = True
#             n = 1
#
#         # 如果程序不在可以运行的时间，那么明显线程已经中断，把is_running设置为False
#         if not is_true_time():
#             is_running = False
#
#             while n:
#                 s = send_email("1974410167@qq.com",f'签到系统已关闭。is_running:{is_running},is_true_time:{is_true_time()}')
#                 s.send()
#                 n = n-1
#
#         time.sleep(30)







