import sys
from PyQt5.QtWidgets import *
import prj.Kiwoom
import time
from pandas import DataFrame
import datetime

# from prj.Kiwoom import *          1
# import prj.Kiwoom                 2
# import prj.Kiwoom as kw           3

MARKET_KOSPI = 0
MARKET_KOSDAQ = 10

class PyMon:
    def __init__(self):
        self.wait_time = 0.4
        self.kiwoom = prj.Kiwoom.Kiwoom()  # 경로와 모듈이름 모두 표시
    #   self.kiwoom = Kiwoom()              1
    #               = prj.Kiwoom.Kiwoom()   2
    #               = kw.Kiwoom()           3
        self.kiwoom.comm_connect()
        self.get_code_list()



    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date':[], 'open': [], 'high': [], 'low':[], 'close': [], 'volume':[]}

        self.kiwoom.set_input_value("종목코드", code)        # 종목코드 어디서 가져오는가? -> 개발가이드를 보거나 / KOA Studio를 볼 것
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(self.wait_time)

        df = DataFrame(self.kiwoom.ohlcv, columns=['open','high','low','close','volume'],
                       index=self.kiwoom.ohlcv['date'])
        return df

    def check_speedy_rising_volume(self, code):
        today = datetime.datetime.today().strftime("%Y%m%d")
        df = self.get_ohlcv(code, today)
        volumes = df['volume']

        if len(volumes) < 21:
            return False

        sum_vol20 = 0
        today_vol = 0

        for i, vol in enumerate(volumes):
            if i == 0:
                today_vol = vol

            elif 1 <= i <= 20:
                sum_vol20 += vol

            else:
                break

        avg_vol20 = sum_vol20 / 20
        if today_vol > avg_vol20 * 10:
            return True

    def update_buy_list(self, buy_list):
        f = open("buy_list.txt","wt")
        for code in buy_list:
            f.writelines("매수;", code, ";시장가;10;0;매수전")
        f.close()


    def run(self):
        buy_list = []
        num = len(self.kospi_codes)

        for i, code in enumerate(self.kospi_codes):
            print(i, '/', num)

            if self.check_speedy_rising_volume(code):
                buy_list.append(code)
                print("급등주 : ", code)

        self.update_buy_list(buy_list)


        df = self.get_ohlcv("039490","20170321")
        print(df)
        print("run")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pymon = PyMon()
    pymon.run()

