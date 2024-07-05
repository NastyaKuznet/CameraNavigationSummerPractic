from django.urls import path
from . import views

urlpatterns = [
    #path('', views.index),
    path('', views.button_click, name='button_click'),
    path('login/', views.log_out, name='logout'),
]