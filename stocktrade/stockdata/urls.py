from django.urls import path
from .views import home, stockdata, analysis, portfolio, delete, delete_ticker

urlpatterns = [
    path('', home, name='home'),
    path('stockdata.html', stockdata, name='stockdata'),
    path('portfolio.html', portfolio, name='portfolio'),
    path('analysis.html', analysis, name='analysis'),
    path('delete/<stock_id>', delete, name='delete'),
    path('delete_ticker', delete_ticker, name='delete_ticker'),
]
