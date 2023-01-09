from cedar.settings import STATIC_URL
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path("", views.loginView, name="login"),
    path("dashboard/", views.dashboardView, name="dashboard"),
    path("map/", views.mapView, name="map"),
    path("calendar/", views.calendarView, name="calendar"),
    path("cleaning/", views.cleaningView, name="cleaning"),
    path("monthly/", views.monthlyView, name="monthly"),
    path("keys/", views.keysView, name="keys"),
    path("revenue/", views.revenueView, name="revenue"),
    path("tax/", views.taxView, name="tax"),
    path("costs/", views.costsView, name="costs"),
    path("capital/", views.capitalView, name="capital"),
    path("uploaddata/", views.uploadView, name="upload"),
]

admin.site.site_header = 'ADMIN'
