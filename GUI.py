from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys, os

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno, self).__init__(*args,*kwargs)
        self.setWindowTitle("POD_GUI")
        
        titleText = QLabel()
        titleText.setText("RAGBABY")
        titleText.setAlignment(Qt.AlignCenter)
        titleText.setFont(QFont('Comic Sans',50))

        self.subtitleText = QLabel()
        self.subtitleText.setText(" ")
        self.subtitleText.setAlignment(Qt.AlignCenter)
        self.subtitleText.setFont(QFont('Comic Sans',20))
        self.subtitleText.setStyleSheet("QLabel {color : grey}")

        self.encryptedText = QLabel()
        self.encryptedText.setText(" ")
        self.encryptedText.setAlignment(Qt.AlignCenter)
        self.encryptedText.setFont(QFont('Comic Sans',20))
        self.encryptedText.setStyleSheet("QLabel {color : grey}")

        self.decryptedText = QLabel()
        self.decryptedText.setText(" ")
        self.decryptedText.setAlignment(Qt.AlignCenter)
        self.decryptedText.setFont(QFont('Comic Sans',20))
        self.decryptedText.setStyleSheet("QLabel {color : grey}")

        self.messageField = QLineEdit()
        self.messageField.setPlaceholderText("Set message here...")

        self.keyField = QLineEdit()
        self.keyField.setPlaceholderText("Set key here...")

        textFielsLayout = QHBoxLayout()
        textFielsLayout.addWidget(self.messageField)
        textFielsLayout.addWidget(self.keyField)
        textFielsLayoutW = QWidget()
        textFielsLayoutW.setLayout(textFielsLayout)

        self.messageFromFileButton = QFileDialog()
        self.keyFromFileButton = QFileDialog()

        messageFileButton = QPushButton()
        messageFileButton.setText("Get message from file")
        messageFileButton.clicked.connect(self.messageFileClicked)

        keyFileButton = QPushButton()
        keyFileButton.setText("Get key from file")
        keyFileButton.clicked.connect(self.keyFileClicked)

        self.saveButton = QPushButton()
        self.saveButton.setText("Save to file")
        self.saveButton.clicked.connect(self.saveClicked)
        self.saveButton.setEnabled(False)

        self.infoButton = QPushButton()
        self.infoButton.setText("Info")
        self.infoButton.clicked.connect(self.infoClicked)

        buttonsFileLayout = QHBoxLayout()
        buttonsFileLayout.addWidget(messageFileButton)
        buttonsFileLayout.addWidget(keyFileButton)
        buttonsFileLayoutW = QWidget()
        buttonsFileLayoutW.setLayout(buttonsFileLayout)

        encryptButton = QPushButton()
        encryptButton.setText("ENCRYPT")
        encryptButton.clicked.connect(self.encryptClicked)

        decryptButton = QPushButton()
        decryptButton.setText("DECRYPT")
        decryptButton.clicked.connect(self.decryptClicked)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(encryptButton)
        buttonsLayout.addWidget(decryptButton)
        buttonsLayoutW = QWidget()
        buttonsLayoutW.setLayout(buttonsLayout)

        infoButtonsLayout = QHBoxLayout()
        infoButtonsLayout.addWidget(self.saveButton)
        infoButtonsLayout.addWidget(self.infoButton)
        infobuttonsLayoutW = QWidget()
        infobuttonsLayoutW.setLayout(infoButtonsLayout)

        #Main Layout
        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(titleText)
        mainMenu.addWidget(self.subtitleText)
        mainMenu.addWidget(self.encryptedText)
        mainMenu.addWidget(self.decryptedText)
        mainMenu.addWidget(textFielsLayoutW)
        mainMenu.addWidget(buttonsLayoutW)
        mainMenu.addWidget(buttonsFileLayoutW)
        mainMenu.addWidget(infobuttonsLayoutW)

        mainMenuW = QWidget()
        mainMenuW.setLayout(mainMenu)

        self.setCentralWidget(mainMenuW)

    def encryptClicked(self):
        key = self.genKey()
        encrypted = self.encrypt(key)
        self.subtitleText.setText("ENCRYPT MODE")
        self.encryptedText.setText(encrypted)
        self.decryptedText.setText("")
        self.saveButton.setEnabled(True)
    
    def decryptClicked(self):
        key = self.genKey()
        decrypted = self.decrypt(key)
        self.subtitleText.setText("DECRYPT MODE")
        self.decryptedText.setText(decrypted)
        self.saveButton.setEnabled(True)
    
    def messageFileClicked(self):
        self.keyFromFileButton.hide()
        self.messageFromFileButton.show()

        if self.messageFromFileButton.exec():
            files = self.messageFromFileButton.selectedFiles()
            r = open(files[0],'r')
            with r:
                data = r.read()
                self.messageField.setText(data)
    
    def keyFileClicked(self):
        self.messageFromFileButton.hide()
        self.keyFromFileButton.show()
        if self.keyFromFileButton.exec():
            files = self.keyFromFileButton.selectedFiles()
            r = open(files[0],'r')
            with r:
                data = r.read()
                self.keyField.setText(data)
    
    def saveClicked(self):
        f = open("result.txt", "w")
        f.write(str(self.encryptedText.text()))
        f.write("\n"+self.genKey())
        f.close()

    def infoClicked(self):
        info = QMessageBox()
        info.setWindowTitle("Info")
        f = open("info.txt", "r")
        data = f.read()
        info.setText(data)
        info.setFont(QFont('Comic Sans',12))
        info.exec_()

    def genKey(self):
        word = self.keyField.text()
        alphabet = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz'
        newWord = ''
        for x in alphabet:
            for y in word:
                if x == y:
                    alphabet = alphabet.replace(x, '')
        for x in word:
            if not x in newWord:
                newWord = newWord + x               
        newKey = newWord + alphabet
        return newKey
    
    def encrypt(self, key):
        encrypted = ""
        text = self.messageField.text()
        wordCount = 1
        num = 1
        for x in text:
            if x == ' ':
                encrypted += ' '
                wordCount += 1
                num = wordCount
            else:
                position = (key.find(x) + num)
                encrypted += key[position % (len(key))]
                num += 1
        return encrypted
    
    def decrypt(self, key):
        decrypted = ""
        text = self.encryptedText.text()
        wordCount = 1
        num = 1
        for x in text:
            if x == ' ':
                decrypted += ' '
                wordCount += 1
                num = wordCount 
            else:
                position = (key.find(x) - num + len(key))
                decrypted += key[position % len(key)]
                num += 1
        return decrypted
                     
#MAIN
app = QApplication(sys.argv)
window = Okno()
window.setFixedSize(800,400)
window.setStyleSheet("background-color: rgb(255,178,102)")
window.show()

app.exec_()