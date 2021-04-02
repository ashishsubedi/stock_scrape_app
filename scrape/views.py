from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, JsonResponse
import json
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize

from .models import Stock, StockRecord
from .tasks import scrape, symbols_json

class ScrapeView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        symbol = data['symbol']
        if not symbol in symbols_json['symbols']:
            return JsonResponse({'status':'FAILED','message':'Invalid Symbol.','records':None})

        try:
            # records = StockRecord.objects.select_related('stock').filter(stock__name=symbol)
            stock = Stock.objects.get(name=symbol)
            records = stock.records.all()
            return JsonResponse({'status':'SUCCESS','message':'SUCCESS','records':serialize('json',records)},safe=False)
        except Stock.DoesNotExist as e:
            
            scrape.delay(symbol)
            return JsonResponse({'status':'PROCESSING','message':'Data is being scraped. Try again in few minutes.','records':None})

