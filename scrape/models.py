from django.db import models

from django.utils import timezone


class Stock(models.Model):
    STATE_CHOICE = [
        ('fetch','fetch'),
        ('ready','ready'),
        ('error','error')
    ]
    name = models.CharField(max_length=10)

    state = models.CharField(max_length=10,choices=STATE_CHOICE,default='fetch')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    def need_to_update(self):
        return True if timezone.now() >= self.updated_at + timezone.timedelta(hours=8) else False

    

class StockRecord(models.Model):


    date = models.DateField()
    transactions_num = models.FloatField(verbose_name="No of Transactions")
    max_price = models.FloatField(verbose_name="Max Price")
    min_price = models.FloatField(verbose_name="Min Price")
    close_price = models.FloatField(verbose_name="Close Price")
    traded_shares = models.IntegerField(verbose_name="Traded Shares")
    total_amt = models.FloatField(verbose_name="Total Amount")
    prev_close = models.FloatField(verbose_name="Previous Close Price")

    stock = models.ForeignKey(Stock,related_name='records',on_delete=models.CASCADE)



    class Meta:
        ordering = ['-date']
    def get_change(self):
        return self.close_price - self.prev_close
    def get_change_percent(self):
        return (self.close_price - self.prev_close)/(self.close_price*1.0)*100

    
