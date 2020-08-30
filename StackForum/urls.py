from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('sessionval/', views.sessionval, name='sessionval'),

    path('', views.index, name='index'),
    path('askaquestion/', views.askaquestion, name='askaquestion'),
    path('postanswer/', views.postanswer, name='postanswer'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('vote/', views.vote, name='vote'),
    path('answervote/', views.answervote, name='answervote'),
    path('test/', views.test, name='test'),
    
    path('answer/<str:id>/', views.answer, name='answer'),

    path('recent/', views.recent, name='recent'),
    path('mostAnswered/', views.mostAnswered, name='mostAnswered'),
    path('mostVisited/', views.mostVisited, name='mostVisited'),
    path('mostPopular/', views.mostPopular, name='mostPopular'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)