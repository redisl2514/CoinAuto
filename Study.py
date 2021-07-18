import requests
from bs4 import BeautifulSoup


DEFAULT = ['KRW-BTC', 'KRW-ETH', 'KRW-XRP', 'KRW-BCH', 'KRW-LTC']


def get_tickers_by_market_cap_rank(num=5):
    try:
        url = "https://coinmarketcap.com/ko/"
        resp = requests.get(url)
        html = resp.text
        soup = BeautifulSoup(html, "html5lib")
        tags = soup.select("#currencies > tbody > tr > td.no-wrap.text-right.circulating-supply > span > span.hidden-xs")
        tickers_by_market_cap = [tag.text for tag in tags]
        upbit_tickers_by_market_cap = [ 'KRW-' + ticker for ticker in tickers_by_market_cap[:num]]
        return upbit_tickers_by_market_cap
    except:
        return DEFAULT


if __name__ == "__main__":
   tickers = get_tickers_by_market_cap_rank()
   print(tickers) 
    
-------------------------------------------------------

import pyupbit
import datetime


def get_break_out_range(ticker, k = 0.5):
    """
    변동성 돌파 전략 목표가를 계산하는 함수
    :param ticker:
    :param k:
    :return:
    """
    try:
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        df = pyupbit.get_ohlcv(ticker, interval="day", count=5)

        if date in df.index:
            today = df.iloc[-1]
            yesterday = df.iloc[-2]
            gap = yesterday['high'] - yesterday['low']
            break_out_range = today['open'] + gap * k
            return break_out_range
        else:
            return None
    except:
        return None


if __name__ == "__main__":
    ticker = "KRW-BTC"
    break_out_range = get_break_out_range(ticker)
    print(break_out_range)
    
-------------------------------------------------------
    
import pyupbit
import datetime
import time
import larry
import manager

TICKER = "KRW-BTC"
FIAT = "KRW"

upbit = manager.create_instance()
break_out_range = larry.get_break_out_range(TICKER)

hold = False

while True:
    now = datetime.datetime.now()

    # 매도
    if now.hour == 8 and now.minute == 50 and (0 <= now.second <= 10):
        if hold is True:
            coin_size = upbit.get_balance(TICKER)
            upbit.sell_market_order(TICKER, coin_size)
            hold = False

        time.sleep(10)

    # 목표가 갱신
    if now.hour == 9 and now.minute == 0 and (0 <= now.second <= 10):
        break_out_range = larry.get_break_out_range(TICKER)

        # 정상적으로 break out range를 얻은 경우
        if break_out_range is not None:
            time.sleep(10)

    # 매수 시도
    cur_price = pyupbit.get_current_price(TICKER)
    if hold is False and cur_price is not None and cur_price >= break_out_range:
        krw_balance = upbit.get_balance(FIAT)
        upbit.buy_market_order(TICKER, krw_balance)
        hold = True

    # 상태 출력
    manager.print_status(TICKER, hold, break_out_range, cur_price)
    time.sleep(1)

-------------------------------------------------------

import pyupbit

def create_instance():
    with open("upbit.txt") as f:
        lines = f.readlines()
        key = lines[0].strip()
        secret = lines[1].strip()

    inst = pyupbit.Upbit(key, secret)
    return inst

def print_status(ticker, hold, break_out_range, cur_price):
    if hold is True:
        status = "보유 중"
    else:
        status = "미보유 중"

    print("코인: {:>10} 목표가: {:>8} 현재가: {:>8} {}".format(ticker, int(break_out_range), int(cur_price), status))

if __name__ == "__main__":
    inst = create_instance()
    print(inst.get_balance("KRW"))
    print_status(True, 100.0, 90.0)
