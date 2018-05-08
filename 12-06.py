import sys

from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtGui import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")

        self.kiwoom.OnEventConnect.connect(self.event_connect)
        self.kiwoom.onReceiveTrData.connect(self.receive_tr_data)


        self.setWindowTitle("pyStock")
        self.setGeometry(100,100,300,150)

        label = QLabel('종목코드 : ',self)
        label.move(20,20)

        self.code_edit = QLineEdit(self)
        self.code_edit.move(80,20)
        self.code_edit.setText("039490")

        btn1 = QPushButton("조회",self)
        btn1.move(190,20)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10,60,280,80)
        self.text_edit.setEnabled(False)


    def event_connect(self,err_code):
        if err_code == 0:
            self.text_edit.append("로그인 성공")

    def receive_tr_data(self,scr_no,rq_name, tr_code, record_name, pre_next, unused1, unused2, unused3, unused4, unused5):
        if rq_name == "opt10001_req":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", tr_code, "", rq_name, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", tr_code, "", rq_name, 0, "거래량")

            self.text_edit.append("종목명 : " + name.strip())
            self.text_edit.append("거래명 : " + volume.strip())



if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_window = MyWindow()
    my_window.show()
    app.exec_()

