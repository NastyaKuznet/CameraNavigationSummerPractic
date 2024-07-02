from django.urls import path
from .views import register, UserLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', register, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='register/login/'), name='logout'),
    #path('logout/', logout_view, name='logout'),
]