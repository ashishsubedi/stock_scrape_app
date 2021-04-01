import django_tables2 as tables
from scrape.models import StockRecord

class StockRecordTable(tables.Table):
    class Meta:
        model = StockRecord
        template_name = "django_tables2/bootstrap.html"
        exclude = ('id',)
