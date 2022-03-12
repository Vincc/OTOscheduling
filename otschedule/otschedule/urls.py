from django.contrib import admin
from django.urls import include, path
#base level url setup
urlpatterns = [
    path('otrender/', include('otrender.urls')),
    path('admin/', admin.site.urls),
    
]
