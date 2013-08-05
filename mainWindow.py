# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class MainWindow
# Author:      Niels Jacot
# Date:        12.07.2013
#################################################################




#import
import sys
import os
import sip
sip.setapi('QVariant', 2) # Set the QVariant v2 for PyQt
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *

#local import
import constante
import deviceControl
import dialogueConnect

# Global variable
POS_X = 250
POS_Y = 250
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200



class MainWindow(QtGui.QMainWindow):
	def __init__(self):
		# Constructor
		
		super(MainWindow,self).__init__()
		self.deviceController = deviceControl.DeviceControl(self)
		
		self.naoIP = None
		self.naoPort = None
		
		# QSettings: used to save nao's ip and port between two application launch
		# Values will be store in the registry
		self.settings = QtCore.QSettings("HE-ARC", "Leap Nao")
		self.initUI()
		
		self.createActions()
		self.createMenubar()
		self.createStatusbar()
		self.createToolbar()
		
	def initUI(self):
		self.setGeometry(POS_X, POS_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
		self.setWindowTitle('Leap Nao')  
		self.setWindowIcon(QtGui.QIcon("images/icon2.png"))
		
		self.mainWidget = QtGui.QWidget(self)
		self.setCentralWidget(self.mainWidget)
		
		self.btnModeWalk = QtGui.QPushButton('Walk', self)
		self.btnModeHead = QtGui.QPushButton('Head', self)
		self.btnModeArm = QtGui.QPushButton('Arm', self)
		self.btnInit = QtGui.QPushButton('Init', self)
		self.btnHand = QtGui.QPushButton('Hand', self)
		
		self.btnModeWalk.setMinimumWidth(70)
		self.btnModeWalk.setMinimumHeight(70)
		
		self.btnModeHead.setMinimumWidth(70)
		self.btnModeHead.setMinimumHeight(70)
		
		self.btnModeArm.setMinimumWidth(70)
		self.btnModeArm.setMinimumHeight(70)
		
		self.btnInit.setMinimumWidth(70)
		self.btnInit.setMinimumHeight(70)
		
		self.btnHand.setMinimumWidth(70)
		self.btnHand.setMinimumHeight(70)
		
		# Set Icon to all buttons
		self.btnModeWalk.setIcon(QIcon("images/down.png"))
		self.btnModeHead.setIcon(QIcon("images/up.png"))
		self.btnModeArm.setIcon(QIcon("images/right.png"))
		self.btnInit.setIcon(QIcon("images/left.png"))
		self.btnHand.setIcon(QIcon("images/space.png"))
		
		# Disabled buttons
		self.btnModeWalk.setDisabled(True)
		self.btnModeHead.setDisabled(True)
		self.btnModeArm.setDisabled(True)
		self.btnInit.setDisabled(True)
		self.btnHand.setDisabled(True)
		
		# Set shortcut to all buttons
		self.btnInit.setShortcut('Left')
		self.btnModeWalk.setShortcut('Down')
		self.btnModeHead.setShortcut('Up')
		self.btnModeArm.setShortcut('Right')
		self.btnHand.setShortcut('Space')
		
		# Connect slot to all buttons
		self.btnModeWalk.clicked.connect(self.buttonClicked)
		self.btnModeHead.clicked.connect(self.buttonClicked)
		self.btnModeArm.clicked.connect(self.buttonClicked)
		self.btnInit.clicked.connect(self.buttonClicked)
		self.btnHand.clicked.connect(self.buttonClicked)
		
		# Layout
		hbox = QtGui.QHBoxLayout()
		hbox.addWidget(self.btnInit)
		hbox.addWidget(self.btnModeWalk)
		hbox.addWidget(self.btnModeHead)
		hbox.addWidget(self.btnModeArm)
		hbox.addWidget(self.btnHand)
		self.mainWidget.setLayout(hbox)
			
	def createMenubar(self):
		self.menubar = self.menuBar()
		
		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(self.launchLeapAction)
		self.fileMenu.addAction(self.connectNaoAction)
		self.fileMenu.addAction(self.turnOffAction)
		self.fileMenu.addAction(self.turnOnAction)
		self.fileMenu.addAction(self.launchVisualizer)
		self.fileMenu.addAction(self.exitAction)
		
		self.helpMenu = self.menubar.addMenu('&Help')
		self.helpMenu.addAction(self.helpAction)
		self.helpMenu.addAction(self.aboutAction)
		
	def createActions(self):
		# Action to leave the application
		self.exitAction = QtGui.QAction(QtGui.QIcon('images/exit.png'), "&Exit", self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.setStatusTip('Exit application')
		self.exitAction.triggered.connect(QtGui.qApp.quit)
		
		# Help action
		self.helpAction = QtGui.QAction(QtGui.QIcon('images/help.png'), "&Help", self)
		self.helpAction.setStatusTip('Help application')
		self.helpAction.triggered.connect(self.slotHelp)
		
		# About Action
		self.aboutAction = QtGui.QAction(QtGui.QIcon('images/about.png'), "&About", self)
		self.aboutAction.setStatusTip('about Leap with Nao')
		self.aboutAction.triggered.connect(self.slotAbout)
		
		# Launch Leap
		self.launchLeapAction = QtGui.QAction(QtGui.QIcon('images/leap.jpg'), "&Launch Leap", self)
		self.launchLeapAction.setStatusTip('about Leap with Nao')
		self.launchLeapAction.triggered.connect(self.slotRunLeap)
		
		# Launch Leap VisualiZer
		self.launchVisualizer = QtGui.QAction(QtGui.QIcon('images/visualizer.jpg'), "&Launch Visualizer", self)
		self.launchVisualizer.setStatusTip('Launch Visualizer')
		self.launchVisualizer.triggered.connect(self.slotRunVisualizer)
		
		#connect Nao Proxy
		self.connectNaoAction = QtGui.QAction(QtGui.QIcon('images/connect.png'), "&Connect Nao", self)
		self.connectNaoAction.setStatusTip('Connect Nao motion Proxy')
		self.connectNaoAction.triggered.connect(self.slotOpenDialogue)
		
		#Turn off nao's motors
		self.turnOffAction = QtGui.QAction(QtGui.QIcon('images/sleep.png'), "&Turn off Nao", self)
		self.turnOffAction.setStatusTip("Turn off all nao's motors")
		self.turnOffAction.triggered.connect(self.turnOffNao)
		self.turnOffAction.setDisabled(True)
		
		#Turn on nao's motors
		self.turnOnAction = QtGui.QAction(QtGui.QIcon('images/motorOn.png'), "&Turn on Nao", self)
		self.turnOnAction.setStatusTip("Turn on all nao's motors")
		self.turnOnAction.triggered.connect(self.turnOnNao)
		self.turnOnAction.setDisabled(True)
		
		
	def createStatusbar(self):
		self.statusBar()
		
	def createToolbar(self):
		self.toolBar = QtGui.QToolBar()
		
		self.toolBar.addAction(self.connectNaoAction)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.launchLeapAction)
		self.toolBar.addAction(self.launchVisualizer)
		self.toolBar.addSeparator()
		self.toolBar.addAction(self.turnOffAction)
		self.toolBar.addAction(self.turnOnAction)
		
		self.addToolBar(self.toolBar)
		
	def slotOpenDialogue(self):
		# Read previous IP and port 
		robotIP, port = self.readPreviousIp()
		
		dialogueIP = dialogueConnect.DialogueConnect(robotIP, port, self)
		if dialogueIP.exec_():
		
			self.naoIP = dialogueIP.lineEditIP.text()
			self.naoPort = dialogueIP.lineEditPort.text()
			
			# Write IP and port
			self.writeNewIP(self.naoIP,self.naoPort)
			
			self.connectNao()
			
	def turnOffNao(self):
		reply = QtGui.QMessageBox.question(self, 'Message',
			"Voulez-vous vraiment éteindre tous les moteurs de nao? Si tel est le cas, prenez soin de soutenir nao pour ne pas qu'il tombe", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			
		if reply == QtGui.QMessageBox.Yes:
			self.deviceController.turnOffNao()
		
	def turnOnNao(self):
		
		self.deviceController.turnOnNao()
		
	def connectNao(self):
		if self.deviceController.connectNao(str(self.naoIP),int(self.naoPort)) != 0:
			msgBox = QtGui.QMessageBox.critical(self, "Error", "Connection with nao is impossible")
			
		self.updateStateButton()
        
		
	def slotRunLeap(self):
		reply = QtGui.QMessageBox.question(self, 'Message',
			" Est-ce que la Leap Motion est connectée ?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)
			
		if reply == QtGui.QMessageBox.Yes:
			self.deviceController.connectLeap() 
		else:
			QtGui.QMessageBox.information(self,'Attention', "Please connect the Leap")
			
	def slotRunVisualizer(self):
		os.startfile("C:\Program Files (x86)\Leap Motion\Leap Services\VisualizerApp.exe")
		
	def slotHelp(self):
		try:
			os.startfile(os.path.normpath("documents/userGuide.pdf"))
		except:
			QtGui.QMessageBox.critical(self, "Error", "User guide not found")
			
	def slotAbout(self):
		QtGui.QMessageBox.about(self, "Leap with Nao", " Cette application utilise la Leap Motion dans le but de contrôler le robot humanoide Nao.<br />"
														"Ce travail a été réalisé par Niels Jacot dans le cadre de son travail de Bachelor à la HE-Arc en Suisse.<br />"
														"Juillet 2013")
		
	def buttonClicked(self):
		
		sender = self.sender()
		if sender == self.btnModeWalk:
			self.deviceController.changeMode(constante.WALK_MODE)
		elif sender == self.btnModeHead:
			self.deviceController.changeMode(constante.HEAD_MODE)
		elif sender == self.btnModeArm:
			self.deviceController.changeMode(constante.ARM_MODE)
		elif sender == self.btnInit:
			self.deviceController.changeMode(constante.INIT_MODE)
		elif sender == self.btnHand:
			self.deviceController.changeMode(constante.HAND_MODE)
			
	def updateStateButton(self):
		if self.deviceController.naoConnect:
			self.btnModeWalk.setEnabled(True)
			self.btnModeHead.setEnabled(True)
			self.btnModeArm.setEnabled(True)
			self.btnInit.setEnabled(True)
			self.btnHand.setEnabled(True)
			
			self.turnOnAction.setEnabled(True)
			self.turnOffAction.setEnabled(True)
		
	def writeNewIP(self, ip, port):
		self.settings.setValue("Nao/ip", ip)
		self.settings.setValue("Nao/port", port)
		
	def readPreviousIp(self):
		ip = self.settings.value("Nao/ip", None)
		port = self.settings.value("Nao/port", None)
		return ip, port
	
	def closeEvent(self, event):
		print"close"
		#if self.deviceController.leapManager.isStarted():
		self.deviceController.leapManager.stopLeap()
		self.deviceController.leapManager.controller.remove_listener(self.deviceController.leapManager)
		#self.deviceController.leapManager.terminate()
			
		'''if self.deviceController.leapManager.isFinished():
			print"fini"
			event.accept()'''

		

def main():
	# Create a QApplication
	Qapplication = QtGui.QApplication(sys.argv)
	
	# Create the main window and display it
	window = MainWindow()
	window.show()
	window.raise_()
	sys.exit(Qapplication.exec_())
	
if __name__ == '__main__':
	main()