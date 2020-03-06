#! /usr/bin/env python3
from common import *
import common
import handlers
import scanner


running = True

def get_stock_buy_list():
    if os.getenv('stock_buy'):
        return os.getenv('stock_buy')
    else:
        return ticker_data.get_name(create=True)


def GetTime():
    return datetime.datetime.now().strftime("%H:%M:%S on %m/%d/%Y")

@click.command()
@click.option('--load', '-l', is_flag=True, help='load data from "dataframe"')
@click.option('--save', '-s', is_flag=True, help='save data to "dataframe"')
@click.option('--interval', '-I', default=60, help='delay between timepoints')
@click.option('--timepoints', '-t', default=5, help='timepoints to use for regression')
@click.option('--index', '-i', default='sp500', help='index or ticker list to scan: def=sp500')
@click.option('--excel', '-x', is_flag=True, help='save data to dataframe.xls')
def main(load, save, interval, timepoints, index, excel):
    'Main status command'

    print('Market Status by Christopher M Palmieri')
    ib.Connect(allow_error=True)
    market_close = datetime.datetime.now().replace(hour=23, minute=59)

    running = False if load else True
    first_time = True
    while (running or first_time) and datetime.datetime.now() < market_close:
        first_time = False
        #get_market_status()

        tickers = ticker_data[index]
        assert tickers, f'Index {index} not found: exiting'

        if load:
            print('\nLoading saved data from dataframe.sav')
            df = pd.read_pickle('dataframe.sav')
            stocks = scanner.ProcessTickerData(df)
        else:
            df = scanner.scan_index(tickers, timepoints, interval, save=save)
            stocks = scanner.ProcessTickerData(df)

        sectors = scanner.get_sector_slopes(stocks)
        handlers.launch(stocks, sectors)

    if excel: scanner.save_xls(df, stocks, sectors)

if __name__ == '__main__':
    main()