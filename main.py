import os
import sys
import json
import random

from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QRadioButton

from utils import base
from utils import htmle
from utils import url
from utils import unicode
from utils import hex
from utils import jwt
from utils import binary
from utils import octal


executing_dir = os.path.dirname(sys.argv[0])

gui_class = uic.loadUiType(os.path.join(executing_dir, "gui/main.ui"))[0]

ALGORITHMS = {
    "base64": base,
    "html": htmle,
    "url": url,
    "unicode": unicode,
    "hex": hex,
    "bin": binary,
    "octal": octal
}

class Encoder(QMainWindow, gui_class):
    
    def __init__(self, parent=None, clipboard=None):
        
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.clipboard = clipboard

        self.algorithm = None
        self.action = None

        # Buttons

        self.cmdEncode.clicked.connect(lambda x: self.encode_decode("encode"))
        self.cmdDecode.clicked.connect(lambda x: self.encode_decode("decode"))
        self.cmdO2I.clicked.connect(self.out2in)
        self.cmdCopy.clicked.connect(self.copy)

        self.cmdDecodeJwt.clicked.connect(self.jwt_decode)

        self.txtJwtHeader.textChanged.connect(self.jwt_decoded_changed)
        self.txtJwtPayload.textChanged.connect(self.jwt_decoded_changed)

        self.txtInput.textChanged.connect(self.input_changed)
        self.txtOutput.textChanged.connect(self.info)

        # Labels

        self.lblInfoInput.setText("Lenght: 0")
        self.lblInfoOutput.setText("Lenght: 0")


    def random_choice(self, params, **kwargs):
        buffer = ""
        for _ in params:
            if random.randint(0, 1):
                buffer += self.algorithm.encode(_, **kwargs)
            else:
                buffer += _
        return buffer


    def call_function(self, function, param, times):
        if self.checkRandom.isChecked():
            function = self.random_choice

        buffer = param
        for _ in range(times):
            buffer = function(buffer, sep=self.txtSeparator.text())
        return buffer


    def encode_decode(self, option="encode"):
        self.action = option
        self.get_algorithm()
        times = 1
        if self.checkDouble.isChecked():
            times = 2
        
        to_encode = self.txtInput.toPlainText()
        if option == "encode":
            encoded = self.call_function(self.algorithm.encode, to_encode, times)
        else:
            encoded = self.call_function(self.algorithm.decode, to_encode, times)
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


    def jwt_decode(self):
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
        

    def jwt_decoded_changed(self):
        header = self.txtJwtHeader.toPlainText()
        payload = self.txtJwtPayload.toPlainText()
        signature = self.txtJwtSignature.toPlainText()

        self.changed = True
        encoded = jwt.encode(header, payload, signature)
        self.txtJwtEncoded.setPlainText(encoded)
    

    def input_changed(self):
        self.encode_decode(self.action)


    def info(self):
        input_text = self.txtInput.toPlainText()
        output_text = self.txtOutput.toPlainText()
        self.lblInfoInput.setText("Lenght: {0}, words: {1}".format(len(input_text), len(input_text.split(" "))))
        self.lblInfoOutput.setText("Lenght: {0}, words: {1}".format(len(output_text), len(output_text.split(" "))))


app = QApplication(sys.argv)
clipboard = app.clipboard()
gui = Encoder(None, clipboard)
gui.show()
app.exec_()
