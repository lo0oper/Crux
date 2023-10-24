from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
urlpatterns = [
    path("home", views.home,name="home"),
    path("csv", views.CSVView.as_view(),name="csv_endpoint"),
    path("healthcheck",views.health_check,name="healthcheck")
]
