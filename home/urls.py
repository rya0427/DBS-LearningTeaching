from django.http.response import HttpResponseNotAllowed
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
   path('', views.home,name="homepage"),
   path('login/', views.loginUser.as_view(), name = "loginUser"),
   path('total/', views.total, name = "total"),
   path('', views.logoutUser, name = "logout"),
   path('dkmh/', views.dkmh, name = "dkmh"),
   path('dk/<str:mamh>/',views.dangky, name='dangky'),
   path('dkerror/', views.dkerror, name='dangkyloi'),
   path('qlgiangday/', views.qlgiangday, name = "qlgiangday"),
   path('qlmonhoc/<str:khoa>/', views.qlmonhoc, name = "qlmonhoc"),
   path('updatemonhoc/<str:khoa>/<str:monhoc>/', views.updateMonhoc, name = "updateMonhoc"),
   path('qllophoc/<str:khoa>/', views.qllophoc, name = "qllophoc"),
   path('updatelophoc/<str:khoa>/<str:lop>/', views.updateLophoc, name = "updateLophoc"),
   path('deletelophoc/<str:khoa>/<str:lop>/', views.deleteLophoc, name = "deleteLophoc"),
   path('newlophoc/<str:khoa>/', views.newLophoc, name = "newLophoc"),
   path('qlgiaotrinh/<str:gv>/', views.qlgiaotrinh, name = "qlgiaotrinh"),
   path('updategiaotrinh/<str:gv>/<str:monhoc>/', views.updategiaotrinh, name = "updategiaotrinh"),
]
