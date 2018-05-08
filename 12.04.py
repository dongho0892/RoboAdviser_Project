import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('pystock')
        self.setGeometry(100,100,300,150)

        self.kiwoom = QAxWidget('KHOPENAPI.KHOpenAPICtrl.1')

        btn1 = QPushButton('Login',self)
        btn1.move(20,20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton('check state', self)
        btn2.move(20,70)
        btn2.clicked.connect(self.btn2_clicked)

    def btn1_clicked(self):
#        pass
#        print('로그인 버튼이 클릭되었습니다.')
        ret = self.kiwoom.dynamicCall("CommConnect()")


    def btn2_clicked(self):
#        pass
#        print('상태 체크 버튼이 클릭되었습니다.')
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not connected")
        else:
            self.statusBar().showMessage("Connected")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_window = MyWindow()
    my_window.show()
    app.exec_()

