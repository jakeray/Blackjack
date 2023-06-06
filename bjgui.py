import sys
from blackjack import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, ourPlayer, parent=None):
        self.ourPlayer = ourPlayer
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle("LeviStars Blackjack")
        self.playTab = playWindow()
        self.loginTab = loginWindow()
        self.startLoginWindow()

    def centerWindow(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def startplayTab(self):
        self.ourPlayer.name = self.loginTab.nameentrybox.text()
        self.playTab.setupPlay(self, self.ourPlayer)
        self.show()

    def startLoginWindow(self):
        self.loginTab.setupLogin(self)
        self.loginTab.pushButton1.clicked.connect(self.startplayTab)
        self.show()

class playWindow(object):
    def __init__(self, ):
        self.playerName = "placeholder"

    def setupPlay(self,MainWindow, ourPlayer):
        MainWindow.setFixedSize(1000,1050)
        MainWindow.centerWindow()
        
        self.centralwidget = QWidget(MainWindow)
        
        self.background = QWidget(self.centralwidget)
        self.background.setGeometry(0,0,1000,1000)
        self.background.setStyleSheet("QWidget {background-image: url(./Images./blackjacktable.png); background-repeat:none}")
        strtouse = '<font color="Black">Player Name: ' + ourPlayer.name + ' | Bankroll: ' + str(ourPlayer.bankroll) + ' | Wager: ' + str(ourPlayer.currentwager)
        self.budgetLabel = QLabel(strtouse,self.centralwidget)
        self.budgetLabel.setFont(QFont("Sanserif", 10))
        self.budgetLabel.setStyleSheet("QLabel {background-color: white}")
        self.budgetLabel.setGeometry(0,1000,1000,50)
        
        MainWindow.setCentralWidget(self.centralwidget)




class loginWindow(object):
    def setupLogin(self,MainWindow):
        
        MainWindow.setGeometry(0, 0, 400, 400)
        MainWindow.setFixedSize(400,400)
        MainWindow.centerWindow()
        

        #MainWidget
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "background-color : #73242a;"
            )
        

        MainWindow.setCentralWidget(self.centralwidget)

        #TitleLabel
        self.titleLabel = QLabel('<font color="white">LeviStars Blackjack')
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setFont(QFont("Sanserif", 15))

        self.nameLabel = QLabel('<font color="white">Enter your name:')
        self.nameLabel.setFont(QFont("Sanserif", 10))

        #NameEntryBox
        self.nameentrybox = QLineEdit()
        self.nameentrybox.setStyleSheet("background-color : white;")

        #PlayButton
        self.pushButton1 = QPushButton('Play')
        self.pushButton1.setStyleSheet(
            "background-color : white;"
            )

        outsidelayout = QVBoxLayout(self.centralwidget)
        insidelayout = QHBoxLayout()

        outsidelayout.addWidget(self.titleLabel)
        insidelayout.addWidget(self.nameLabel)
        insidelayout.addWidget(self.nameentrybox)
        outsidelayout.addLayout(insidelayout)
        outsidelayout.addWidget(self.pushButton1)

    








