from django.contrib import admin
from .models import User,CourseMessage
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

class CourseMessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(User,UserAdmin)
admin.site.register(CourseMessage,CourseMessageAdmin)