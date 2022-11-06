
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete/<str:pk>', views.delete, name='delete'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login')
]