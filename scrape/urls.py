
from django.contrib import admin
from django.urls import path, include

from .views import ScrapeView

urlpatterns = [
    path('<name>/',ScrapeView.as_view())
]
