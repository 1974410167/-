from django.urls import path
from . import views

app_name = "app1"
urlpatterns = [

    path('index/',views.index,name='index_url'),
    path('login/',views.login.as_view(),name='login_url'),
    path('register/',views.register.as_view(),name='register_url'),
    path('center/<int:account>/',views.personal_center.as_view(),name='center_url'),
    path('quit/', views.quit_center.as_view(), name='quit_url'),
    path('handle/',views.handle.as_view(),name='handle')

]