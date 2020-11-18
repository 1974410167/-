from django.urls import path
from . import views

app_name = "app1"
urlpatterns = [
    path('index/',views.index,name='index_url'),
    path('login/',views.login,name='login_url'),
    path('register/',views.register.as_view(),name='register_url'),
    path('center/<int:account>/',views.Personal_center,name='center_url')
]