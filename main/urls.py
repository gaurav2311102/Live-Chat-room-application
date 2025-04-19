from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from main.views import create_superuser_view 
urlpatterns = [
    
    path('',views.home,name = "home"),
    path('login',views.UserLogin,name='login'),
    path('signup',views.SignupCreteView.as_view(),name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('user-profile/<int:pk>',views.user_profile,name='user-profile'),
    path('room/<int:pk>/',views.room,name='room'),
    path('create-room',views.RoomCreateView.as_view(),name = "create-room"),
    path('update-room/<int:pk>',views.UpdateRoom,name='update-room'),
    path('delete-room/<int:pk>',views.RoomDeleteView.as_view(),name='delete-room'),
#  path('create_message',views.create_message,name='create_message'),
    path('update-message/<int:pk>/',views.update_message,name='update-message'),
    path('delete-message/<int:pk>/',views.MessageDeleteView.as_view(),name='delete-message'),
    path('join-room/<int:pk>',views.join_room,name='join-room'),
    path('leave-room/<int:pk>',views.leave_room,name='leave-room'),
    path('create-superuser/', create_superuser_view, name='create-superuser'),
    
     
 ]
 
   