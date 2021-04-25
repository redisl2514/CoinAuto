import pyupbit
import time

ticker = "KRW-NEO"

def get_target_price(ticker): #변동성 돌파 전략. 목표가 계산하기 (S)
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close'] #당일 시가
    yesterday_high = yesterday['high'] #전일 고가
    yesterday_low = yesterday['low'] #전일 저가
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]

ma5 = get_yesterday_ma5(ticker)
target_price = get_target_price(ticker)

while True:
    try:
        current_price = pyupbit.get_current_price(ticker)
        if (current_price > target_price) and (current_price > ma5):
            print("종목 :", ticker)
            print("목표가 돌파했습니다")
        else:
            print("종목 :", ticker)
            print("변동성 전략 목표가 :", target_price)
            print("5일 이동평균 목표가 :", ma5)
    except:
        print("에러 발생")
    time.sleep(5)