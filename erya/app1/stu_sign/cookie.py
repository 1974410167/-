import execjs
import requests
import os


def confirm(cookies):
    if "UID" not in cookies:
        return False
    else:
        return True

module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir,'test.js')


class generate_Cookies():

    def __init__(self,user,password):
        self.user = user
        self.password = password

    def get_decode_password(self):
        """
        加密密码
        :return:
        """
        try:
            with open(file_path,encoding='utf-8') as f:
                print('ssssssssss')
                ctx = execjs.compile(f.read())
                print('qqqqqqqqqqqqq')
                self.password = ctx.call("getPwd", self.password)
                print(self.password)
        except:
            print("密码加密失败")

    def get_cookies(self):
        """
        获得cookies,并写入本地
        :return:
        """
        self.get_decode_password()
        try:

            from_data = {
                "fid": "4311",
                'uname': self.user,
                'password': self.password,
                'refer': 'http%3A%2F%2Fi.mooc.chaoxing.com',
                't': 'true',
            }
            url = "https://passport2.chaoxing.com/fanyalogin"
            r = requests.post(url, data=from_data)
            cookieJar = r.cookies
            cookies = requests.utils.dict_from_cookiejar(cookieJar)

            if not confirm(cookies):
                print("账号或密码错误，无法获得有效cookie!请重新输入！")
                return None
            else:
                return cookies

        except Exception as e:
            print(e)


s = generate_Cookies('15738698290','wsghy.5637')
m = s.get_cookies()
print(m)

