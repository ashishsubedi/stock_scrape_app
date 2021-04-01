from django.shortcuts import render
from django.http import HttpResponse
from django_tables2 import SingleTableView, RequestConfig

from scrape.models import StockRecord, Stock
from .tables import StockRecordTable

def indexView(request):
    return render(request,'homepage/index.html')

class StockRecordListView(SingleTableView):
    model = StockRecord
    table_class = StockRecordTable
    template_name = 'homepage/stockrecord_list.html'
    
def tableView(request,name):
    if name == "":
        name = request.GET.get('name','None')

    stock = Stock.objects.filter(name=name).first()
    if stock:
        table = StockRecordTable(stock.records.all())
        RequestConfig(request).configure(table)
    
        return HttpResponse(table.as_html(request))
    table = StockRecordTable('')
    RequestConfig(request).configure(table)
    return HttpResponse(table.as_html(request))
