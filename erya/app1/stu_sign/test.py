
from concurrent.futures import ThreadPoolExecutor
import random
import time
import redis
import threading
# pool = redis.ConnectionPool(host='localhost',port=6379,decode_responses=True)
# r = redis.Redis(connection_pool=pool)

list = {'name':"Ss",'age':'11'}

a = list

a.pop('name')

print(a)
print(list)



#
# r.flushdb()
# def a():
#     n = 1000
#     while n:
#         t = r.lpop('list1')
#         print(t)
#         n=n-1
#
#
# def b():
#     n = 1000
#     while n:
#         t = r.lpush('list1',n)
#         print(t)
#         n = n-1

# m = threading.Thread(target=a,args=())
# n = threading.Thread(target=b,args=())
# n.start()
# m.start()
# n.join()
# m.join()
#
# print('ssssssssssssss')
# print(r.llen('list1'))
# print('ssssssssssss')
# print(r.lrange('list1',0,-1))







# list = []
#
#
# for i in range(10000):
#     t = random.randint(1,5)
#     list.append(t)
#
#
#
# def a(i):
#
#     print('开始')
#     time.sleep(i)
#     print('完成')
#
# time1 = time.time()
#
# with ThreadPoolExecutor(max_workers=1000) as f:
#
#     f.map(a,list)
#
# end = time.time()
#
# print(end-time1)
