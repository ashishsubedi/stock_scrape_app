from django.urls import path, include, re_path
from .views import indexView
from django.views.generic import TemplateView
from .views import  StockRecordListView, tableView

urlpatterns = [
    path('',TemplateView.as_view(template_name ='homepage/index.html')),
    path('stocks/<name>',tableView, name='stock_record_table')

]
