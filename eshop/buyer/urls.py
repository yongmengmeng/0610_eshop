from django.urls import path, re_path
from buyer.views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('active/', ActiveView.as_view()),
    path('index/', IndexView.as_view()),
    path('detail/', DetailView.as_view()),
]
