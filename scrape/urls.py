
from django.contrib import admin
from django.urls import path, include

from .views import IndexView

urlpatterns = [
    path('<pk>/',IndexView.as_view())
]
