import execjs
import requests
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; ELE-AL00 Build/HUAWEIELE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1178 MMWEBSDK/200201 Mobile Safari/537.36 MMWEBID/616 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
}

class CookieError(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)  # 初始化父类
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


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
                ctx = execjs.compile(f.read())
                self.password = ctx.call("getPwd", self.password)
        except:
            print("密码加密失败")

    def get_cookies(self):
        """
        获得cookies,并写入本地
        :return:
        """
        try:
            print(self.user)
            print(self.password)
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
            if "UID" not in cookies:
                print("账号或密码错误，无法获得有效cookie!请重新输入！")

                raise CookieError("账号密码错误")

            else:
                print("你的身份资料验证完毕，键入任何值继续....")
                input('键入任何值继续....')
                cookies = str(cookies)
                with open('cookies.txt','a+') as f:
                    f.write(cookies)
                    f.write('\n')
                    print(f"用户{self.user}已写入cookies.txt文件")
                return cookies
        except Exception as e:
            print(e)

    def __call__(self, *args, **kwargs):
        self.get_decode_password()
        self.get_cookies()

user = input("输入尔雅账号：")
password = input('输入尔雅密码：')

s = generate_Cookies(user,password)
s()



