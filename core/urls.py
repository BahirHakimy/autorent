from .views import hello_world
from django.urls import path
from django.conf import settings


urlpatterns = [path("", hello_world)]
