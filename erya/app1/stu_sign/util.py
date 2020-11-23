import requests
import re

headers = ''
cookies = ''
# import sys
# print(sys.path)

class util_1():

    def __init__(self):
        self.headers = headers
        self.cookies = cookies

    def get_mycourse_list(self):
        """
        由cookie获得课程列表
        [{'courseid': 215462815, 'name': '测试', 'teacherfactor': '葛浩源', 'classid': 34337550}, {'courseid': 214753207, 'name': '20-21-1Mysql数据库', 'teacherfactor': '王方', 'classid': 32406600}, {'courseid': 214750284, 'name': '形势与政策', 'teacherfactor': '李斌', 'classid': 32398991}, {'courseid': 214708614, 'name': '大学英语A（Ⅲ）', 'teacherfactor': '赵伟', 'classid': 32289817}, {'courseid': 214705044, 'name': '离散数学', 'teacherfactor': '徐莹莹', 'classid': 32280857}, {'courseid': 214662732, 'name': '软件构造', 'teacherfactor': '桑园', 'classid': 32179615}, {'courseid': 214574474, 'name': '软件工程', 'teacherfactor': '宋利敏', 'classid': 31964197}, {'courseid': 214571869, 'name': 'Web前端设计（英）', 'teacherfactor': '邵彧', 'classid': 31957181}, {'courseid': 214384398, 'name': '2020-2021-1Web程序设计（JSP）', 'teacherfactor': '周喜平', 'classid': 31509796}, {'courseid': 214321332, 'name': '全国大学英语四级课程（Cet-4）', 'teacherfactor': '秦玉', 'classid': 31508455}, {'courseid': 92065860, 'name': '计算机网络--郑州西亚斯学院在线开放课程', 'teacherfactor': '师晓利、谢泽奇、郭利周、李铁盘、丁小娜、李永、王芳', 'classid': 31318982}, {'courseid': 213281256, 'name': '操作系统期末考试', 'teacherfactor': '刘莹', 'classid': 29333145}, {'courseid': 212960292, 'name': '返校复学第一课', 'teacherfactor': '郑州西亚斯学院', 'classid': 28566410}, {'courseid': 208938249, 'name': '计算机组成原理 2019-2020年第二学期', 'teacherfactor': '王伟铮', 'classid': 18127279}, {'courseid': 208849360, 'name': '2019-2020-2 操作系统', 'teacherfactor': '贾庆节', 'classid': 17927617}, {'courseid': 208847704, 'name': '数据库课程设计', 'teacherfactor': '数据库教研室', 'classid': 17923997}, {'courseid': 208589513, 'name': '大学体育（四）', 'teacherfactor': '刘莉莉', 'classid': 17260401}, {'courseid': 208308347, 'name': '19-20-2马克思主义基本原理概论', 'teacherfactor': '刘元元', 'classid': 16682270}, {'courseid': 208085285, 'name': '大学英语A（Ⅳ）', 'teacherfactor': '秦玉', 'classid': 16238587}, {'courseid': 204865291, 'name': '19-20-1思想道德修养与法律基础', 'teacherfactor': '', 'classid': 9662912}, {'courseid': 204683416, 'name': '2019-2020-1大学物理', 'teacherfactor': '杨铁柱', 'classid': 9257113}, {'courseid': 204671661, 'name': '计科物理实验2019', 'teacherfactor': '田壮壮', 'classid': 9231021}, {'courseid': 204069931, 'name': '2019年SIAS微课-《复杂句分析》', 'teacherfactor': '张丽', 'classid': 8135906}, {'courseid': 202259462, 'name': '新视野大学英语（1）', 'teacherfactor': '吴娇娇', 'classid': 6180513}, {'courseid': 202012162, 'name': '《计算机导论》2018-2019-1', 'teacherfactor': '张高杰', 'classid': 4748343}]
        :return:
        """
        my_scource_url = "http://mooc1-api.chaoxing.com/mycourse/backclazzdata?view=json&rss=1"

        try:
            r = requests.get(my_scource_url,headers=self.headers,cookies=self.cookies)
            print(r.text)

            r.encoding='utf-8'
            scource_dict = r.json()

            message_list = []

            # 遍历所有课程，把所有课程都加入到list
            for item in scource_dict['channelList']:
                if ("course" not in item['content']):
                    continue
                pushdata = {}
                pushdata['courseid'] = item['content']['course']['data'][0]['id']
                pushdata['name'] = item['content']['course']['data'][0]['name']
                pushdata['teacherfactor'] = item['content']['course']['data'][0]['teacherfactor']
                pushdata['classid'] = item['content']['id']
                message_list.append(pushdata)
            return message_list

        except:
            print("获得课程列表失败！")

    def get_uid(self):
        """
        获得uid
        :param cookie_dict:
        :return:
        """
        try:
            uid = self.cookies.get("UID")
            return uid
        except Exception:
            print("获得uid失败")

    def taskactivatelist(self,courseId,classId,uid):
        """
        得到每个课程的所有活动任务,存放activeId
        :return:
        """
        try:
            avtivate_list = []

            url="https://mobilelearn.chaoxing.com/ppt/activeAPI/taskactivelist?courseId="+str(courseId)+"&classId="+str(classId)+"&uid="+uid
            r = requests.get(url,headers=self.headers,cookies=self.cookies)
            course_dict = r.json()
            for item in course_dict["activeList"]:
                if item['status'] == 1 and item["activeType"]==2:
                    str_url = item["url"]

                    def get_activateId():
                        nonlocal str_url
                        """
                        从url字符串中提取activateId
                        :param str:
                        :return:
                        """
                        compile = re.compile("activePrimaryId=(\d+)&")

                        activateId = compile.findall(str_url)[0]

                        return activateId

                    activateId = get_activateId()
                    avtivate_list.append(activateId)

            return avtivate_list

        except Exception as e:
            print(e)

    def sign(self,activateId,uid,name):
        """
        由activateId和uid进行签到
        :param activateId:
        :param uid:
        :return:
        """
        url = "https://mobilelearn.chaoxing.com/pptSign/stuSignajax?activeId="+activateId+"&uid="+uid+"&clientip=&latitude=-1&longitude=-1&appType=15&fid=0"
        r = requests.get(url,headers=self.headers,cookies=self.cookies)
        if r.text=="success":
            print("================================")
            print(f'{name}签到成功')
            print("================================")

            return True



