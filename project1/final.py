import os
import json

BASEDIR = ''
DATDIR = os.path.join(BASEDIR, 'data')
TICPATH = os.path.join(BASEDIR, 'TICKERS.txt')

COLUMNS = ['Volume', 'Date', 'Adj Close', 'Close', 'Open', 'High']
COLWIDTHS = {'Volume': 14, 'Date': 11, 'Adj Close': 19, 'Close': 10, 'Open': 6, 'High': 20}


def get_tics(pth):
    tics_dict = {}
    with open(pth, 'r') as file:
        for line in file:
            exchange, ticker = line.replace('"', '').strip().split('=')
            tics_dict[ticker.lower()] = exchange.lower()
    return tics_dict


def read_dat(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def line_to_dict(line):
    data_dict = {}
    start = 0
    for column in COLUMNS:
        end = start + COLWIDTHS[column]
        data_dict[column] = line[start:end].strip()
        start = end
    return data_dict


def verify_tickers(tic_exchange_dic, tickers_lst=None):
    if tickers_lst:
        for ticker in tickers_lst:
            if ticker not in tic_exchange_dic:
                raise ValueError(f"Ticker {ticker} is not valid.")


def verify_cols(col_lst=None):
    if col_lst:
        for col in col_lst:
            if col not in COLUMNS:
                raise ValueError(f"Column {col} is not valid.")


def create_data_dict(tic_exchange_dic, tickers_lst=None, col_lst=None):
    data_dict = {}
    for ticker, exchange in tic_exchange_dic.items():
        if tickers_lst and ticker not in tickers_lst:
            continue
        data_list = []
        filepath = os.path.join(DATDIR, f"{ticker}_prc.dat")
        for line in read_dat(filepath):
            data = line_to_dict(line)
            if col_lst:
                data = {col: data[col] for col in col_lst if col in data}
            data_list.append(data)
        data_dict[ticker] = {'exchange': exchange, 'data': data_list}
    return data_dict


def create_json(data_dict, pth):
    with open(pth, 'w') as f:
        json.dump(data_dict, f, indent=4)


if __name__ == "__main__":
    tic_exchange_dic = get_tics(TICPATH)
    data_dict = create_data_dict(tic_exchange_dic)
    json_output_path = os.path.join(BASEDIR, 'result.json')
    create_json(data_dict, json_output_path)
    print(f"JSON file has been saved to: {json_output_path}")
