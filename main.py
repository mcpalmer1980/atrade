#! /usr/bin/env python3
from common import *
import common
import algos
import scanner

running = True

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
        scanner.print_market_status()
        tickers = ticker_data[index]
        #common.ib.SellAll()
        ib.Buy('AAPL', 20)

        df = scanner.scan_index(tickers, timepoints, interval, load=load, save=save)
        stock_frame = scanner.ProcessTickerData(df)

        sector_frame = scanner.get_sector_slopes(stock_frame)
        algos.launch(stock_frame, sector_frame)

    scanner.save_xls(excel, df, stock_frame, sector_frame)

if __name__ == '__main__':
    main()