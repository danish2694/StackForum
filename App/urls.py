from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sessionval/', views.sessionval, name='sessionval'),

    path('', views.index, name='index'),
    path('askaquestion/', views.askaquestion, name='askaquestion'),
    path('postanswer/', views.postanswer, name='postanswer'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    
    path('logout/', views.logout, name='logout'),
    
    path('answer/<str:id>/', views.answer, name='answer'),

    path('profile/<str:id>', views.profile, name='profile'),
    path('recent/', views.recent, name='recent'),
    path('mostAnswered/', views.mostAnswered, name='mostAnswered'),
    path('mostVisited/', views.mostVisited, name='mostVisited'),
    path('mostPopular/', views.mostPopular, name='mostPopular'),


]