# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class DeviceControl
# Author:      Niels Jacot
# Date:        12.07.2013
#################################################################



# local import
import naoMove
import leapManage
import constante
import collisionDetect

# import
import sys
import Leap
import sip
sip.setapi('QVariant', 2)
from PyQt4 import QtCore, QtGui



class DeviceControl():
	# Class used to make link between Leap and Nao
	
	def __init__(self, parent = None):
		# Constructor
		
		self.naoConnect = False
		self.parent = parent
		self.test=True
		
		self.naoMoveManage = naoMove.NaoMove(self.parent)
		self.leapManager = leapManage.LeapManage(self.naoMoveManage, self, self.parent)
		
		self.sensorManage = collisionDetect.CollisionDetect()
		self.sensorConnected = False
		
	def connectNao(self,IP,PORT):
		if self.naoMoveManage.connect(IP,PORT) == 0:
			self.naoConnect = True
			
			if self.sensorManage.connect(IP, PORT) == 0:
				self.sensorConnected = True
			else:
				self.sensorConnected = False
			return 0
		else:
			return 1
		
	def connectLeap(self):
		self.leapManager.start()
				
		
	def changeMode(self, mode):
	
		# If we are already in the same mode, nothing is done
		if self.leapManager.currentMode != mode:
			
			if self.leapManager.currentMode == constante.WALK_MODE and mode != constante.HEAD_MODE:
				self.leapManager.currentMode = mode
				self.leapManager.walk = False
				
			elif mode == constante.HEAD_MODE and self.leapManager.currentMode == constante.WALK_MODE:
				self.leapManager.currentMode = mode
				self.leapManager.walk = False
				self.naoMoveManage.detectFace()
				
			elif mode == constante.HEAD_MODE and self.leapManager.currentMode != constante.WALK_MODE:
				self.leapManager.currentMode = mode
				self.naoMoveManage.detectFace()
				
			elif self.leapManager.currentMode == constante.HEAD_MODE:
				self.naoMoveManage.behaviourProxy.stopBehavior("faceDetect")
				self.leapManager.currentMode = mode
				
			else:
				self.leapManager.currentMode = mode
		
	def turnOffNao(self):
		if self.naoConnect:
			self.naoMoveManage.stiffnessOff()
			
	def turnOnNao(self):
		self.naoMoveManage.testMotorOn()