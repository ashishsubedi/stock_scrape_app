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
    try:
        # stock = Stock.objects.filter(name=name).first()

        # if stock:
        records = StockRecord.objects.select_related('stock').filter(stock__name=name)
        table = StockRecordTable(records)
        RequestConfig(request).configure(table)
    
        return HttpResponse(table.as_html(request))
    except Exception as e:
        print("Error",e)
        table = StockRecordTable('')
        RequestConfig(request).configure(table)
        return HttpResponse(table.as_html(request))
