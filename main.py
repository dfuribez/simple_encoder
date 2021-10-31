import os
import sys
import json

from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton

from utils import base
from utils import htmle
from utils import url
from utils import unicode
from utils import hex
from utils import jwt


executing_dir = os.path.dirname(sys.argv[0])

gui_class = uic.loadUiType(os.path.join(executing_dir, "gui/main.ui"))[0]

ALGORITHMS = {
    "base64": base,
    "html": htmle,
    "url": url,
    "unicode": unicode,
    "hex": hex
}

class Encoder(QMainWindow, gui_class):
    
    def __init__(self, parent=None, clipboard=None):
        
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.clipboard = clipboard

        self.algorithm = None

        # Buttons

        self.cmdEncode.clicked.connect(lambda x: self.encode_decode("encode"))
        self.cmdDecode.clicked.connect(lambda x: self.encode_decode("decode"))
        self.cmdO2I.clicked.connect(self.out2in)
        self.cmdCopy.clicked.connect(self.copy)

        self.txtJwtEncoded.textChanged.connect(self.jwt_changed)
    

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
    
    
    def copy(self):
        self.clipboard.setText(self.txtOutput.toPlainText())


    def jwt_changed(self):
        token = self.txtJwtEncoded.toPlainText()
        header, payload, signature = jwt.process(token)

        try:
            pretty_payload = json.dumps(json.loads(payload), indent=2, sort_keys=False)
        except:
            pretty_payload = payload
        
        try:
            pretty_header = json.dumps(json.loads(header), indent=2, sort_keys=False)
        except:
            pretty_header = header

        self.txtJwtHeader.setPlainText(pretty_header)
        self.txtJwtPayload.setPlainText(pretty_payload)
        self.txtJwtSignature.setPlainText(signature)
        


app = QApplication(sys.argv)
clipboard = app.clipboard()
gui = Encoder(None, clipboard)
gui.show()
app.exec_()
