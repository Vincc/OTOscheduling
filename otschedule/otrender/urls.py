from django.urls import path
from . import views

urlpatterns = [

    path('', views.renderTimes, name = 'renderTimes'),
    path('changePassword', views.change_Password, name = 'changePassword'),
    path('login', views.login_request, name='login'),
    path("logout", views.logout_request, name= "logout"),
    path("changeSchedule", views.scheduleSettings, name= "changeSchedule"),
    
    path("deleteDate/<int:id>/", views.deleteDate, name='deleteDate'),
    path("deleteTime/<int:id>/", views.deleteTime, name='deleteTime'),
    
]