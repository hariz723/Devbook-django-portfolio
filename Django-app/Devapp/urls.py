from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerUser, name="register"),
    path('',views.home,name="home"),
    path('room/<str:pk>/',views.room,name="room"),
    path('create-room/',views.CreateRoom, name="Create-Room"),
    path('updated-room/<str:pk>/',views.UpdatedRoom, name="Updated-Room"),
    path('delete-room/<str:pk>/',views.DeleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/',views.deletemessage, name="delete-message"),
]