from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class StockRecord(models.Model):


    date = models.DateField()
    transactions_num = models.FloatField(verbose_name="No of Transactions")
    max_price = models.FloatField(verbose_name="Max Price")
    min_price = models.FloatField(verbose_name="Min Price")
    close_price = models.FloatField(verbose_name="Close Price")
    traded_shares = models.FloatField(verbose_name="Traded Shares")
    total_amt = models.IntegerField(verbose_name="Total Amount")
    prev_close = models.FloatField(verbose_name="Previous Close Price")

    stock = models.ForeignKey(Stock,related_name='records',on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
    def get_change(self):
        return self.close_price - self.prev_close
    def get_change_percent(self):
        return (self.close_price - self.prev_close)/(self.close_price*1.0)*100

