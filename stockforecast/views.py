import os
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from stockforecast.models import Stock, StockPrice
from .scrape_bursa_malaysia import *
from django.core.paginator import Paginator
from .utils import save_stock_data_from_csv
from .lstm import *
from django.db.models import Q


# Create your views here.
def stockscreener(request):

    stocks = Stock.objects.all()

    # if not Stock.objects.exists():
    #     scrape_stock_list()
    #     stocks = Stock.objects.all()

    context = {"stocks": stocks}
    paginator = Paginator(stocks, 50)
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    return render(request, "stockscreener/stocklist.html", context)

def stock_detail(request, symbol):
    stock = get_object_or_404(Stock, symbol=symbol)
    stock_prices = StockPrice.objects.filter(stock=stock)

     # Get the forecasted values for the stock
    forecasts = LstmForecastedValue.objects.filter(stock=stock)
    forecasts_mlp = MLPForecastedValue.objects.filter(stock=stock)

    if not stock_prices.exists():
        context = {'stock': stock, 'stock_prices': stock_prices}
        return render(request, 'stockscreener/stock_detail.html', context)
    
    context = {'stock': stock, 'stock_prices': stock_prices, 'forecasts': forecasts, 'mlp': forecasts_mlp,}
    return render(request, 'stockscreener/stock_detail.html', context)

