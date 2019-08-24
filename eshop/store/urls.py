from django.urls import path,re_path
from store.views import *

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('index/',IndexView.as_view()),
    path('base/',BaseView.as_view()),
]
