from django.urls import path, re_path
from store.views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    # path('base/',BaseView.as_view()),
    path('add/store/', AddStoreView.as_view()),
    path('edit/store/', EditStoreView.as_view()),
    path('add/goods/', AddGoodsView.as_view()),
    path('list/goods/', ListGoodsView.as_view()),
    path('', IndexView.as_view()),
]
