from cedar.settings import STATIC_URL
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    #
    path("upload/", views.upload, name="upload"),
    path("createexptype/", views.createExpType, name="createexptype"),
    path("addexp/", views.addExp, name="addexp"),
    path("deleteexpense/", views.deleteExp, name="deleteexpense"),
    path("deletecapexpense/", views.deleteCapExp, name="deletecapexpense"),
    path("savenote/", views.addNote, name="addnote"),
    path("enablekey/", views.enableKey, name="enableKey"),
]

admin.site.site_header = 'ADMIN'
