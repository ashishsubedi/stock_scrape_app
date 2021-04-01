from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Stock

class IndexView(DetailView):
    queryset = Stock.objects.all()
    model = Stock
