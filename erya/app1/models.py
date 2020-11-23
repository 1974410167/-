from django.db import models
# Create your models here.


class CourseMessage(models.Model):

    courseid = models.CharField(max_length=20)
    classid = models.CharField(max_length=20)
    coursename = models.CharField(max_length=30)
    teacherfactor = models.CharField(max_length=30)
    pub_data = models.DateField(auto_now=True)

    def __str__(self):
        return self.coursename

    class Meta:
        ordering = ['pub_data']


class User(models.Model):

    account = models.CharField(max_length=30,db_index=True)
    password = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    uid = models.CharField(max_length=20)

    balance = models.IntegerField(null=True,default=0)
    is_vip = models.BooleanField(default=True)
    pub_data = models.DateField(auto_now=True)

    is_activates = models.JSONField(default=dict)
    course_message = models.ManyToManyField(CourseMessage,blank=True)

    def __str__(self):
        return self.account

    class Meta:
        ordering = ['pub_data']




