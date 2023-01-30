from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow
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
    QLineEdit
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
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        # Create and connect widgets
        self.clicksLabel = QLabel("Counting: 0 clicks", self)
        self.clicksLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.stepLabel = QLabel("Long-Running Step: 0", self)
        self.stepLabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.countBtn = QPushButton("Stop!", self)
        self.countBtn.clicked.connect(self.countClicks)
        self.longRunningBtn = QPushButton("Run Dice!", self)
        self.longRunningBtn.clicked.connect(self.runLongTask)
        # Set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.clicksLabel)
        layout.addWidget(self.countBtn)
        layout.addStretch()
        layout.addWidget(self.stepLabel)
        layout.addWidget(self.longRunningBtn)
        self.le = QLineEdit('apikey', self)
        self.le.resize(550, 30)
        self.centralWidget.setLayout(layout)
        status = QStatusBar()
        status.showMessage("Status")
        self.setStatusBar(status)

    def countClicks(self):
        global enabled
        enabled = False
        self.clicksCount += 1
        self.clicksLabel.setText(f"Counting: {self.clicksCount} clicks")

    def reportProgress(self, n):
        self.stepLabel.setText(n)

    def runLongTask(self):
        global enabled
        global API_KEY
        enabled = True
        API_KEY = self.le.text()
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
win = Window()
win.show()
sys.exit(app.exec())