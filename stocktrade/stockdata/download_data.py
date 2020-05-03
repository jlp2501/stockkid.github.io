import quandl
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import figure
import io
import base64


def download_data(ticker, **kwargs):
    """
    Download financial data using quandl and clean data by dropping NA values
    :param ticker:
    :param kwargs:
    :return: dataframe
    """
    enter_ticker = "WIKI/" + ticker
    quandl.ApiConfig.api_key = "WmTEx2dyXqQ-Xd9iShT7"
    ticker_data_df = quandl.get(enter_ticker, start_date='2000-01-01', end_date='2018-01-01')
    ticker_data_df_adj_clo = ticker_data_df[['Adj. Close']]
    ticker_data_df_adj_clo = ticker_data_df_adj_clo.dropna(0)
    return ticker_data_df_adj_clo


def data_fitting(df):
    """
    Splitting dataframe to training and testing datasets, perform model fitting on the datasets,
    and output plot for visualization purpose
    :param df:
    :return: image
    """
    train_data = df[:int(df.shape[0]*0.7)]
    test_data = df[int(df.shape[0]*0.7):]

    train_rolling_30_days_mean = train_data.rolling(30).mean()
    train_rolling_30_days_dev = 2*train_data.rolling(30).std()

    train_upper = (train_rolling_30_days_mean+train_rolling_30_days_dev)
    train_lower = (train_rolling_30_days_mean-train_rolling_30_days_dev)

    test_rolling_30_days_mean = test_data.rolling(30).mean()
    test_rolling_30_days_dev = 2*test_data.rolling(30).std()

    test_upper = (test_rolling_30_days_mean + test_rolling_30_days_dev)
    test_lower = (test_rolling_30_days_mean - test_rolling_30_days_dev)

    plt.figure(figsize=(30, 15), facecolor='black', edgecolor='black')
    plot_mean_train = plt.plot(train_rolling_30_days_mean, label='Train Mean', color='dimgrey', linewidth=1)
    plot_upper_train = plt.plot(train_upper, label='Train Upper Bound', color='royalblue', linewidth=1)
    plot_lower_train = plt.plot(train_lower, label='Train Lower Bound', color='maroon', linewidth=1)

    plot_mean_test = plt.plot(test_rolling_30_days_mean, label='Test Mean', color='darkslategrey', linewidth=1)
    plot_upper_test = plt.plot(test_upper, label='Train Upper Bound', color='turquoise', linewidth=1)
    plot_lower_test = plt.plot(test_lower, label='Train Lower Bound', color='coral', linewidth=1)

    plot_actual_test_val = plt.plot(test_data, label='Actual Test Values', color='navy', linewidth=1)

    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.title('30-Day Moving Average Model')

    file_ = io.BytesIO()
    plt.savefig(file_)
    image_b64 = base64.b64encode(file_.getvalue()).decode()
    image_b64 = f"data:image/jpeg;base64,{image_b64}"
    return image_b64





