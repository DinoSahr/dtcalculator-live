
from django import views
from django.urls import path

from . import views

app_name = 'DTCalculator'
urlpatterns = [
    path('', views.applicationHomeView, name='home'),
    path('about/', views.aboutView, name='about'),
    path('report/', views.reportingViews, name='report'),
]