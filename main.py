import os
import sys

from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton

from utils import base
from utils import htmle
from utils import url

executing_dir = os.path.dirname(sys.argv[0])

gui_class = uic.loadUiType(os.path.join(executing_dir, "gui/main.ui"))[0]

ALGORITHMS = {
    "base64": base,
    "html": htmle,
    "url": url
}

class Encoder(QMainWindow, gui_class):
    
    def __init__(self, parent=None):
        
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.algorithm = None

        # Buttons

        self.cmdEncode.clicked.connect(lambda x: self.encode_decode("encode"))
        self.cmdDecode.clicked.connect(lambda x: self.encode_decode("decode"))
        self.cmdO2I.clicked.connect(self.out2in)
    

    def encode_decode(self, option="encode"):
        self.get_algorithm()
        to_encode = self.txtInput.toPlainText()
        if option == "encode":
            encoded = self.algorithm.encode(to_encode)
        else:
            encoded = self.algorithm.decode(to_encode)
        self.txtOutput.setPlainText(encoded)    


    def get_algorithm(self):
        for algo in self.groupOptions.findChildren(QRadioButton):
            if algo.isChecked():
                self.algorithm = ALGORITHMS[algo.text().lower()]
    

    def out2in(self):
        self.txtInput.setPlainText(self.txtOutput.toPlainText())
        self.txtOutput.setText("")


app = QApplication(sys.argv)
gui = Encoder(None)
gui.show()
app.exec_()