from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('keys', views.keys,name='keys'),
    path('api', views.fetchAPI,name='api'),
    path('stop', views.stopAPI,name='stop'),
    path('reset', views.resetKeys,name='reset'),
]
