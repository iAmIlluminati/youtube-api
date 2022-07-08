from django.urls import path
from . import views
urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('keys', views.keys,name='keys'),
    path('reset', views.resetKeys,name='reset'),
]
