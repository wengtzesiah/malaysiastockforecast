from django.db import models
from django_cryptography.fields import encrypt

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=10)
    lastprice = models.CharField(max_length=255)
    exchange = models.CharField(max_length=50)
    name1 = encrypt(models.CharField(max_length=255, default="NA"))
    name = models.CharField(max_length=255, default="NA")

    def __str__(self):
        return f"{self.symbol}"


class StockPrice(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, default=0)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=6)
    high_price = models.DecimalField(max_digits=10, decimal_places=6)
    low_price = models.DecimalField(max_digits=10, decimal_places=6)
    close_price = models.DecimalField(max_digits=10, decimal_places=6)
    adj_close_price = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    volume = models.IntegerField()

    def __str__(self):
        return f"{self.stock} {self.date} {self.stock.id}"
    
class LstmForecastedValue(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()

    next_1_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    def __str__(self):
        return f"{self.stock.name} - {self.date}"

class MLPForecastedValue(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField()

    next_1_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_day =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_week =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_month =  models.DecimalField(max_digits=10, decimal_places=6, default=0)

    next_1_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_2_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_3_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_4_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    next_5_year = models.DecimalField(max_digits=10, decimal_places=6, default=0)

    def __str__(self):
        return f"{self.stock.name} - {self.date}"
