
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('settings/',views.settings,name='settings'),
    path('data/',views.data,name='data'),
    path('data/<str:ivt>/',views.SeeInventory,name='SeeInventory'),
    path('data/<str:ivt>/<str:itm>/',views.SeeItem,name='SeeItem'),
    path('UpdateIvt/<str:IvtPk>/', views.DeleteIvt, name='DeleteIvt'),
    path('UpdateItm/<str:IvtPk>/<str:ItmPk>', views.DeleteItm, name='DeleteItm'),
    path('UpdateIvt/<str:IvtPk>/<str:NewName>/', views.UpdateIvt, name='UpdateIvt'),
    path('UpdateItm/<str:IvtPk>/<str:ItmPk>/<str:NewName>/', views.UpdateItm, name='UpdateItm'),


]