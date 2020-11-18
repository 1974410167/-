import execjs
import requests

def confirm(cookies):
    if "UID" not in cookies:
        return False
    else:
        return True

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
            with open("./test.js",encoding='utf-8') as f:
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
            print(cookies)
            if not confirm(cookies):
                print("账号或密码错误，无法获得有效cookie!请重新输入！")
                return None
            else:
                return cookies

        except Exception as e:
            print(e)

def sss(n):

    return n


s = generate_Cookies('15738698290','wsghy.5637')
print(s.get_cookies())



