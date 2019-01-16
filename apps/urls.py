from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('GenerateApi/', views.GenerateApi, name='GenerateApi'),
    path('downloadApi/', views.downloadApi, name='downloadApi')
]