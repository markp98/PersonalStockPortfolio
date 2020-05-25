import PySimpleGUI as sg
import pickle
import os
import datetime as dt
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

def choice():
    layout = [

              [sg.Text('Please choose a choice of action!', size=(40, 1))],
              [sg.Checkbox('Add stock')],
              [sg.Checkbox('Delete stock')],
              [sg.Checkbox('Visualize specific stock')],
              [sg.Ok()]

              ]

    window = sg.Window('Your Stock Market Portfolio Menu').Layout(layout)
    event, values = window.Read()
    if values[0]:
        return 1;
    elif values[1]:
        return 2
    elif values[2]:
        return 3;

def add_stock():
    layout = [

              [sg.Text('Enter Stock Ticker'), sg.InputText(size=(15, 1)), sg.Ok()]

             ]

    window = sg.Window('Stock Ticker Entry').Layout(layout)
    event, values = window.Read()

    sg.Popup('Adding ' + values[0] + ' to your portfolio...', title='')
    ticker = values[0].upper()

    with open("your_stock_tickers.pickle", "wb") as f:
        pickle.dump(ticker, f)

    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')

    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now()

    if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
        df = web.DataReader(ticker, 'yahoo', start, end)
        df.to_csv('stock_dfs/{}.csv'.format(ticker))
    else:
        sg.Popup('Already have ' + ticker, title='')

def delete_stock():
    layout = [

        [sg.Text('Enter Stock Ticker to Delete'), sg.InputText(size=(15, 1)), sg.Ok()]

    ]

    window = sg.Window('Stock Ticker Deletion').Layout(layout)
    event, values = window.Read()
    ticker = values[0].upper()
    sg.Popup('Deleting {}s stock info...'.format(ticker), title='')

    try:
        os.remove('stock_dfs/{}.csv'.format(ticker))
    except FileNotFoundError:
        sg.Popup('Could not find {} in portfolio'.format(ticker), title='')


def closing_cost_visualization():
    layout = [

        [sg.Text('Enter stock ticker to visualize'), sg.InputText(size=(17, 1)), sg.Ok()]

    ]

    window = sg.Window('Stock Ticker Entry').Layout(layout)
    event, values = window.Read()
    ticker = values[0].upper()

    try:
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker), parse_dates=True, index_col=0)
        plt.ylabel('Adj Closed Cost')
        df['Adj Close'].plot()
        plt.show()
    except FileNotFoundError:
        sg.Popup('{} has not been added to your portfolio'.format(ticker), title='')



choice = choice()

if choice == 1:
    add_stock()
elif choice == 2:
    delete_stock()
elif choice == 3:
    closing_cost_visualization()

