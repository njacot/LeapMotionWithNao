# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class DialogueConnect
# Author:      Niels Jacot
# Date:        12.07.2013
#################################################################


#import
import re
import sys
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui


class DialogueConnect(QtGui.QDialog):
	# Class used to put IP and port of Nao
	
	def __init__(self, ip, port, parent=None):
		# Constructor
		
		self.ip = ip
		self.port = port
		
		super(DialogueConnect, self).__init__(parent)
		self.setWindowTitle("Nao connection")
		
		self.initUI()
		
	def initUI(self):
		# Labels and LineEdit
		labelIP = QtGui.QLabel("Nao IP: ")
		self.lineEditIP = QtGui.QLineEdit()
		self.lineEditIP.setMaxLength(15)
		self.lineEditIP.setFixedWidth(100)
		
		# Buttons
		btnCancel = QtGui.QPushButton("Cancel")
		btnCancel.clicked.connect(self.reject)
		
		btnConnect = QtGui.QPushButton("Connect")
		btnConnect.setDefault(True)
		btnConnect.clicked.connect(self.slotConnect)
		
		btnHelp = QtGui.QPushButton("Help")
		btnHelp.clicked.connect(self.slotHelp)
		
		
		if self.ip is not None:
			self.lineEditIP.setText(self.ip)
		lblPort = QtGui.QLabel("Nao Port: ")
		self.lineEditPort = QtGui.QLineEdit()
		self.lineEditPort.setMaxLength(5)
		self.lineEditPort.setFixedWidth(50)
		if self.port is not None:
			self.lineEditPort.setText(self.port)
		else:
			self.lineEditPort.setText("9559")
		
		# Layout
		mainLayout=QtGui.QVBoxLayout()
		inputLayout = QtGui.QGridLayout()
		inputLayout.addWidget(labelIP, 0, 0)
		inputLayout.addWidget(self.lineEditIP, 0, 1)
		inputLayout.addWidget(lblPort, 1, 0)
		inputLayout.addWidget(self.lineEditPort, 1, 1)
		
		inputLayout.addWidget(btnHelp, 2, 0 )
		inputLayout.addWidget(btnConnect, 2, 1)
		inputLayout.addWidget(btnCancel, 2, 2)
		
		mainLayout.addLayout(inputLayout)
		mainLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
		self.setLayout(mainLayout)
		
	def slotHelp(self):
		QtGui.QMessageBox.about(self, "Leap with Nao Connection", " Enter a correct IP address look like this one (127.1.1.1)<br />"
														"The port must be a number between 1 and 65535.<br />"
														"If you do not know how to find the IP address of nao, Please look the user guide which is provided with the application")
		
		
	def slotConnect(self):
		if not self.validateIP():
			msgBox = QtGui.QMessageBox.warning(self, "Error", 
										"Wrong IP !\n"
										"IP must look like 127.1.1.1 (each between 0 and 255)")
			self.lineEditIP.setFocus()
			
		elif not self.validatePort():
				msgBox = QtGui.QMessageBox.warning(self, "Error", 
							"Wrong port !\n"
							"Port must be a number between 1 and 65535")
				self.lineEditPort.setFocus()
		else:
			self.accept()
		
	def validatePort(self):
		# Validate port
		port = self.lineEditPort.text()
		try:
			if 1 > long(port) > 65535:
				return False
			else:
				return True
		except:
			return False
			
	def validateIP(self):
		# Validate Ip address
		ip = self.lineEditIP.text()

		parts = ip.split(".")
		if len(parts) != 4:
			return False
		for item in parts:
			try:	
				if not 0 <= int(item) <= 255:
					return False
			except:
				return False
		return True
	
	
