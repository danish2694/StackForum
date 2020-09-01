from django.contrib import admin
from django.urls import path
from VotesApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vote/',views.vote,name='vote'),
    path('answervote/', views.answervote, name='answervote'),
]