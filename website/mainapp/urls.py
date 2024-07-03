from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new/', views.button_click, name='button_click'),
]