import pyupbit
import random
import time
import requests

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text})
    #print(response)

myToken = "xoxb-2214036150211-2213836848130-MGOLLe5LfbVZP5h8buojkHCY"
post_message(myToken, "#stock", "코인 자동매매 시작")

#def dbgout(message):
#    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
#    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
#    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
#    post_message(myToken,"#stock", strbuf)

access = "W0pBEN1VwvBvTHtp8zD2hVfgxufsv0PHzrgwCbaS"
secret = "z0iST1K4uhFwP1QKX8riwXmIPxwRsPu4xnUr9KKw"

tickers = pyupbit.get_tickers(fiat="KRW") #업비트에 있는 원화코인만 검색
random.shuffle(tickers) ## ticker 랜덤으로 Scan 하도록 명령.

#post_message(myToken, "#stock", "종목:" + str(tickers) + "매수 완료")
#post_message(myToken, "#stock", "종목:" + str(tickers) + "매도 완료")

def get_target_price(ticker):
    """종목 5분봉 현재 이전 종가 가격"""
    Y_lp_ma5 = pyupbit.get_ohlcv(ticker, interval="minute5")
    Y_lm5_price = Y_lp_ma5['close'].rolling(5).mean()
    Y_lm5_list = Y_lm5_price.iloc[-2]
    return Y_lm5_list

def get_current_price(ticker):
    """종목 5분봉 현재 가격"""
    Now_lp_ma5 = pyupbit.get_ohlcv(ticker, interval="minute5")
    Now_lm5_price = Now_lp_ma5['close'].rolling(5).mean()
    Now_lm5_list = Now_lm5_price.iloc[-1]
    return Now_lm5_list

def sell_target_price(ticker):
    """종목 5분봉 10일선 현재 가격"""
    Now_lp_ma10 = pyupbit.get_ohlcv(ticker, interval="minute5")
    Now_lm10_price = Now_lp_ma10['close'].rolling(10).mean()
    Now_lm10_list = Now_lm10_price.iloc[-1]
    return Now_lm10_list

def buy_crypto_currency(ticker):
    krw = upbit.get_balance(ticker="KRW")  # 잔고에 남아있는 돈 얻어옴
    buy_price = pyupbit.get_current_price(ticker) #종목 현재가(매수가)
    unit = krw / float(buy_price) #원화 잔고를 최우선 매도가로 나눠서 구매 가능한 수량을 계산
    unit2 = unit - unit * 0.05 #주문 수량에서 수수료(unit * 0.015) 뺀 가격
    upbit.buy_limit_order(ticker, buy_price, unit2) #종목, 매수가, 매수 수량
    #upbit.buy_market_order(ticker, krw)
    #print("%s %s개 매수" % ticker, unit)

def sell_crypto_currency(ticker):
    unit = upbit.get_balance(ticker)
    upbit.sell_market_order(ticker, unit)

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("자동매매 시작")

while True:
    for ticker in tickers:
        target_price = get_target_price(ticker) + get_target_price(ticker) * 0.02
        current_price = get_current_price(ticker)
        sell_price = sell_target_price(ticker)
        try:
            if target_price < current_price:
                buy_crypto_currency(ticker)
                print("종목 :", ticker)
                print("매수 완료")
                post_message(myToken, "#stock", "종목:" + str(ticker) + "매수 완료")
            else:
                if current_price < sell_price:
                    sell_crypto_currency(ticker)
                    print("종목 :", ticker)
                    print("매도 완료")
                    post_message(myToken, "#stock", "종목:" + str(ticker) + "매도 완료")
        except:
            time.sleep(0.5)
    time.sleep(1)
    print("-----------------------잠시 대기 중-----------------------")
    #post_message(myToken, "#stock", "잠시 대기 중")
