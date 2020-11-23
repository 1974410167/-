import redis

class op_redis():

    def __init__(self):

        self.pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
        self.r = redis.StrictRedis(connection_pool=self.pool)

    def get_a_course(self,courseid):

        course_message_dict = self.r.hgetall(courseid)

        return course_message_dict

    def exists(self,courseid):

        if self.r.exists(courseid):
            return True

        else:
            return False

    def set_a_course(self,courseid,course_mess):

        bool_val = self.r.hmset(courseid,course_mess)

        return bool_val



