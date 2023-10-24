from django.contrib import admin
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_protect

urlpatterns = [
    path("home", views.home,name="home"),
    path("csv", views.CSVView.as_view(),name="csv_endpoint"),
    path("csv/data",views.GetCSVData.as_view(),name="get_csv_file_data"),
    path("healthcheck",views.health_check,name="healthcheck"),
]
