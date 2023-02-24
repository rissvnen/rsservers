from django.contrib import admin
from django.urls import path
from Servers import views

app_name = 'Servers'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.index, name='Servers'),
]
