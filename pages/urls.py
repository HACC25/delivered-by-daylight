from django.urls import path
from pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("gemini/", views.gemini_api, name = "gemini_api"),
]
