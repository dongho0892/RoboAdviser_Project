import sys
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

TR_REQ_TIME_INTERVAL = 0.2


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl('KHOPENAPI.KHOpenAPICtrl.1')

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)


    def comm_connect(self):
        self.dynamicCall('CommConnect()')
        self._login_event_loop = QEventLoop()
        self._login_event_loop.exec()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("Connected")
        else:
            print("Disconnected")

        self._login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall('GetCodeListByMarket(QString)', market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall('GetMasterCodeName(QString)', code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall('GetConnectState()')
        return ret

    def set_input_value(self, id, value):
        self.dynamicCall('SetInputValue(QString, QString)', id, value)

    def comm_rq_data(self, rq_name, tr_code, prev_next, screen_no):
        self.dynamicCall('CommRqData(QString, QString, int, QString)',
                         rq_name, tr_code, prev_next, screen_no)
        self._tr_event_loop = QEventLoop()
        self._tr_event_loop.exec()

    def _get_comm_data(self, tr_code, record_name, index, item_name):
        ret = self.dynamicCall('GetCommData(QString, QString, int, QString)',
                               tr_code, record_name, index, item_name)
        return ret

    def _get_repeat_cnt(self, tr_code, record_name):
        ret = self.dynamicCall('GetRepeatCnt(QString, QString)',
                               tr_code, record_name)

    def _receive_tr_data(self, scr_no, rq_name, tr_code, record_name, pre_next,
                         unused1, unused2, unused3, unused4):
        ret = {'scr_no': scr_no, 'rq_name': rq_name, 'tr_code': tr_code,
               'record_name': record_name, 'pre_next': pre_next}
        print(ret)

        if pre_next == '2':
            self.data_remained = True
        else:
            self.data_remained = False

        if rq_name == 'opt10081_req':
            self._opt10081(rq_name, tr_code)

        elif rq_name == "opw00001_req":
            self._opw0001(rq_name, tr_code)
        try:
            self._tr_event_loop.exit()
        except AttributeError:
            pass

    def _opt10081(self, rq_name, tr_code):
        data_cnt = self._get_repeat_cnt(tr_code, rq_name)

        for i in range(data_cnt):
            date = self._get_comm_data(tr_code, rq_name, i, '일자')
            open = self._get_comm_data(tr_code, rq_name, i, '시가')
            high = self._get_comm_data(tr_code, rq_name, i, '고가')
            low = self._get_comm_data(tr_code, rq_name, i, '저가')
            close = self._get_comm_data(tr_code, rq_name, i, '현재가')
            volume = self._get_comm_data(tr_code, rq_name, i, '거래량')

            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))


    def send_order(self, rqname,scr_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(Qstring, Qstring, Qstring, int, QString, int, int, QString, QString)",
                         [rqname, scr_no, acc_no, order_type, code, quantity, price, hoga, order_no])



    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret


    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)",tag)
        return ret


    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def _opw00001(self, rqname, trcode):
        self.d2_deposit = self._get_comm_data(trcode, "",rqname,0,"d+2 추정예수금")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    kiwoom.set_input_value("계좌번호", "8087711111")
    kiwoom.set_input_value("비밀번호","0000")
    kiwoom.comm_rq_data("opw00001_req","opw00001",0,"2000")

    print(kiwoom.d2_deposit)
