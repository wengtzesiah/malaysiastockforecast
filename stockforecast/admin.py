from django.contrib import admin
from .models import *


# Register your models here.
class StockNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')

admin.site.register(Stock, StockNameAdmin)
admin.site.register(StockPrice)
admin.site.register(LstmForecastedValue)
admin.site.register(MLPForecastedValue)

