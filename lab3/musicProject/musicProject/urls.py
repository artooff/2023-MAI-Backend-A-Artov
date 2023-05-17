from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("musicService/", include("musicService.urls")),
    path('admin/', admin.site.urls),
]
