from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
import json
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from .models import Stock, StockRecord
from .tasks import scrape

class ScrapeView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        symbol = data['symbol']
        try:
            stock = Stock.objects.get(name=symbol)
            records = stock.records.all()
            print(records)
            return JsonResponse({'status':'SUCCESS','message':'SUCCESS','records':serialize('json',records)},safe=False)
        except Stock.DoesNotExist as e:
            scrape.delay(symbol)
            return JsonResponse({'status':'FAILED','message':'Data is being scraped. Try again in few minutes.','records':None})

