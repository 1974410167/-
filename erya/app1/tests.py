from django.test import TestCase
from datetime import datetime,timedelta
# Create your tests here.

time = timedelta(days=1)
m = datetime.now()
n = timedelta(days=-1)

print(m+n)

def t():
    time = datetime.now()
    print(time.day)
    print(time.month)
    print(time.year)


