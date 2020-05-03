from django.shortcuts import render, redirect
import json
import requests
from django.contrib import messages
from .forms import StockForm

from .models import Portfolio

from .download_data import download_data, data_fitting


def home(request):
    """
    Add home function to connect to API
    :param request:
    :return: json
    """
    if request.method == "POST":
        ticker = request.POST.get("ticker", "").lower()
        news_request = requests.get('https://cloud.iexapis.com/stable/stock/' + ticker +'/news?token=pk_d140b994384542afb620be54e7f02c58')
        try:
            news_load = json.loads(news_request.content)
        except Exception as error:
            news_load = 'There is an error in your request. Please try again!'
        return render(request, 'home.html', {'news_load': news_load})

    return render(request, 'home.html', {'news_load': []})


def stockdata(request):
    """
    Stockdata function to connect to API
    :param request:
    :return: json
    """
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + ticker + '/quote?token=pk_d140b994384542afb620be54e7f02c58')

        try:
            api_load = json.loads(api_request.content)
        except Exception as error:
            api_load = 'There is an error in your request. Please try again!'

        return render(request, 'stockdata.html', {'api_load': api_load})

    else:
        return render(request, 'stockdata.html', {'ticker': "Enter Your Ticker Above For More Information"})


def portfolio(request):
    """
    Portfolio function to connect to API
    :param request:
    :return: json
    """
    if request.method == 'POST':
        form = StockForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ('Ticker has been added'))
            return redirect('portfolio')
    else:
        ticker = Portfolio.objects.all()
        output = []
        for item in ticker:
            api_request = requests.get('https://cloud.iexapis.com/stable/stock/' + str(item) + '/quote?token=pk_d140b994384542afb620be54e7f02c58')
            try:
                api_load = json.loads(api_request.content)
                output.append(api_load)
            except Exception as error:
                api_load = 'There is an error in your request. Please try again!'

        return render(request, 'portfolio.html', {'ticker': ticker, 'output': output})


def analysis(request):
    """
    Analysis function to connect with data_fitting model and output relevant plot
    :param request:
    :return: plot
    """
    if request.method == "POST":
        ticker = request.POST.get("ticker", "").lower()
        get_data = download_data(str(ticker))
        b64_image = data_fitting(get_data)

        return render(request, 'analysis.html', {"b64_image": b64_image})

    else:
        return render(request, 'analysis.html', {"b64_image": None})

def delete(request, stock_id):
    """
    Delete function to delete item  in  portfolio
    :param request:
    :param stock_id:
    :return: link
    """
    item = Portfolio.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ('Ticker has been deleted!'))
    return redirect(portfolio)


def delete_ticker(request):
    return render(request, 'analysis.html', {})
