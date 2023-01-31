from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QGridLayout
from PyQt5.QtGui import QKeySequence, QPalette, QColor
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QStatusBar,
    QLineEdit,
    QMenuBar,
    QAction,
    QDialog,
    QComboBox,
    QDialogButtonBox,
    QFormLayout,
    QMessageBox
)
import sys
# import cloudscraper
import requests
import os
import sys
import json
import cffi
import _cffi_backend
from curl_cffi import requests

# Step 1: Create a worker class
#

# scraper = cloudscraper.create_scraper()
API_KEY = ""
target = 2.56
condition = 'above'
currency = 'doge'
betamount = 0.00000000


url = "https://stake.games/_api/graphql"
 
body = """
mutation DiceRoll($amount: Float!, $target: Float!, $condition: CasinoGameDiceConditionEnum!, $currency: CurrencyEnum!, $identifier: String!) {\n  diceRoll(\n    amount: $amount\n    target: $target\n    condition: $condition\n    currency: $currency\n    identifier: $identifier\n  ) {\n    ...CasinoBet\n    state {\n      ...CasinoGameDice\n    }\n  }\n}\n\nfragment CasinoBet on CasinoBet {\n  id\n  active\n  payoutMultiplier\n  amountMultiplier\n  amount\n  payout\n  updatedAt\n  currency\n  game\n  user {\n    id\n    name\n  }\n}\n\nfragment CasinoGameDice on CasinoGameDice {\n  result\n  target\n  condition\n}\n"""    

logs = ['<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>', '<tr><td>-<td<tr>']

enabled = True


        
        
class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.setWindowTitle("Settings")
        self.apikey = QLineEdit(self)
        self.basebet = QLineEdit(self)
        self.currency = QComboBox(self)
        self.currency.addItems(['btc', 'eth', 'ltc', 'doge', 'bch', 'xrp', 'trx', 'eos'])
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self);
        
        self.apikey.setFixedWidth(400);
        self.basebet.setFixedWidth(400);
        self.currency.setFixedWidth(100);
        
        self.basebet.setText('0.00000000')
        
        if os.path.isfile('user.json'): 
            f = open("user.json")
            data = json.load(f)
            self.apikey.setText(data["api"])
            self.basebet.setText(data["basebet"])
            index = self.currency.findText(data["currency"], QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.currency.setCurrentIndex(index)
                
        layout = QFormLayout(self)
        layout.addRow("API", self.apikey)
        layout.addRow("BASEBET", self.basebet)
        layout.addRow("CURRENCY", self.currency)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return (self.apikey.text(), self.basebet.text(), str(self.currency.currentText())) 


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def run(self):
        global logs
        global enabled
        """Long-running task."""
       
        while enabled:
        
            resp = requests.post(url=url, headers = {
            'Content-type': "application/json; charset=utf-8",
            'x-access-token': API_KEY},json={"query": body, "variables":{"target":target,"condition":condition,"identifier":"ffeefefeffefefea5","amount":betamount,"currency":currency}}, impersonate="chrome101")

            
            print("response: ", resp.json())
            data = resp.json()
            del logs[0]
            if 'errors' in data:
                logs.append('<tr><td>'+ 'result: ' + str(data["errors"][0]['message'])+'</td></tr>')
            else:
                logs.append('<tr><td>'+ 'result: ' + str(data["data"]["diceRoll"]["state"]["result"])+'</td></tr>')
            html = '<table>'+ ''.join(logs) +'</table>'
            # self.logging.setText(html)
            self.progress.emit(html)
        self.finished.emit()

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.clicksCount = 0
        # self.setupUi()

    # def setupUi(self):
        self.setWindowTitle("Freezing Dice")
        self.resize(550, 350)
        # self.centralWidget = QWidget()
        # self.setCentralWidget(self.centralWidget)
        self.mainbox = QWidget()
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QGridLayout())
        self.setGeometry(200, 200, 700, 400)
        # Create and connect widgets
        self.stepLabel = QLabel("Long-Running Step: 0")
        # self.stepLabel.setAlignment(Qt.AlignBottom)
        self.stepLabel.setStyleSheet('''border :1px; border-radius:5px;
                                        background:rgb(40,40,40);color:rgb(150,150,150)
                                        ''')
        self.mainbox.layout().addWidget(self.stepLabel, 0, 0, 1, 9)

        # self.countBtn = QPushButton("Stop!", self)
        # self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Run Dice!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        self.longRunningBtn.setMaximumSize(130, 30)
        #self.btn.resize(self.btn.sizeHint())
        #self.btn.move(600, 360)
        #self.mainbox.layout().addWidget(0,0,1,8)
        self.mainbox.layout().addWidget(self.longRunningBtn, 1, 8, 1, 1)
        # Set the layout
        # layout = QVBoxLayout()
        
        # layout.addWidget(self.countBtn)
        # layout.addStretch()
        # layout.addWidget(self.stepLabel)
        # layout.addWidget(self.longRunningBtn)
        
        # self.mainbox.setLayout(layout)
        status = QStatusBar()
        status.showMessage("Status")
        self.setStatusBar(status)

        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        menuBar.setNativeMenuBar(False)

        self.settings_action = QAction("&Settings", self)
        menuBar.addAction(self.settings_action)
        self.settings_action.triggered.connect(self.show_settings)

        self.about_action = QAction("&About", self)
        menuBar.addAction(self.about_action)
        self.about_action.triggered.connect(self.show_about_dialog)


    def show_settings(self):
        global API_KEY
        global betamount
        global currency
  
        dialog = InputDialog()
        dialog.apikey.setText(API_KEY)
        dialog.basebet.setText('{:.8f}'.format(betamount))
        index = dialog.currency.findText(currency, QtCore.Qt.MatchFixedString)
        if index >= 0:
            dialog.currency.setCurrentIndex(index)

        #dialog.move(window.mapToGlobal(window.rect().center() - dialog.rect().center()))
        retValue = dialog.exec()
        if retValue == 1:
            inputs = dialog.getInputs()
            API_KEY = inputs[0]
            betamount = float(inputs[1])
            currency = inputs[2]
            json = '{ "api": "' + API_KEY + '", "basebet": "' + '{:.8f}'.format(betamount) + '", "currency": "' + currency + '" }'
            

    def show_about_dialog(self):
        text = "<center>" \
               "<h1>Dice bot :)</h1>" \
               "</center>" \
               "<p>Made by poky1084 &copy; " \
               "Discord: 0000000#7073</p>"
        QMessageBox.about(self, "About", text)


    
    def reportProgress(self, n):
        self.stepLabel.setText(n)

    def runLongTask(self):
        global enabled
        global API_KEY
        enabled = True
        # Step 2: Create a Qhread object
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = Worker()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        # Step 6: Start the thread
        self.thread.start()

        # Final resets
        self.longRunningBtn.setEnabled(False)
        self.thread.finished.connect(
            lambda: self.longRunningBtn.setEnabled(True)
        )
        # self.thread.finished.connect(
            # lambda: self.stepLabel.setText("Long-Running Step: 0")
        # )



app = QApplication(sys.argv)

app.setStyle("Fusion")
# font.setStyleHint(QFont::TypeWriter);

palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
win = Window()
win.show()
sys.exit(app.exec())