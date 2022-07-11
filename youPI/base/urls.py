from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.dashboard,name='dashboard'),
    path('<int:page>', views.dashboard,name='dashboard'),

    path('keys', views.keys,name='keys'),
    path('reset', views.resetKeys,name='reset'),


    path('api', views.fetchAPI,name='api'),
    # TODO Need to configure way to stop BG process
    path('stop', views.stopAPI,name='stop'),

    path('reset', views.resetKeys,name='reset'),

]
