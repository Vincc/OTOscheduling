from django.urls import path
from . import views

#create url patterns list with path, view function and url path name
urlpatterns = [

    path('', views.renderTimes, name = 'renderTimes'),
    path('changePassword', views.change_Password, name = 'changePassword'),
    path('login', views.login_request, name='login'),
    path("logout", views.logout_request, name= "logout"),
    path("changeSchedule", views.scheduleSettings, name= "changeSchedule"),
    path("deleteDate/<int:id>/", views.deleteDate, name='deleteDate'),
    path("deleteTime/<time>/", views.deleteTime, name='deleteTime'),
    
]
