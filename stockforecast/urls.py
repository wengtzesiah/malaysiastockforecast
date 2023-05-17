from django.urls import include, path
from . import views

urlpatterns = [ 
    path('stockscreener', views.stockscreener, name="stockscreener"), 
    path('stock/<str:symbol>/', views.stock_detail, name='stock_detail'),
    
]