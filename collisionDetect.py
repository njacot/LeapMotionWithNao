# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class CollisionDetect
# Author:      Niels Jacot
# Date:        12.07.2013
#################################################################

# import
from naoqi import ALProxy


class CollisionDetect():
	# Class used to have values from sensor's feet
	
	def __init__(self):
		# Constructor
		
		self.memoryProxy = None
		
		
		rightFootSensorL = "Device/SubDeviceList/RFoot/Bumper/Left/Sensor/Value"
		rightFootSensorR = "Device/SubDeviceList/RFoot/Bumper/Right/Sensor/Value"
		leftFootSensorL = "Device/SubDeviceList/LFoot/Bumper/Left/Sensor/Value"
		leftFootSensorR = "Device/SubDeviceList/LFoot/Bumper/Right/Sensor/Value"
		
		self.listSensorNames = [leftFootSensorL, leftFootSensorR, rightFootSensorL, rightFootSensorR]
		
	def connect(self, robotIP, port):
		# Connect to the Memory Proxy of Nao
		
		
		try:
			self.memoryProxy = ALProxy("ALMemory", robotIP, port)
		except:
			return 1
		return 0

		
	def getFeetSensor(self):
		# Return a list with last values of feet sensor 
		
		values = []
		for n in self.listSensorNames:
			values.append(self.memoryProxy.getData(n, 0))
			
		return values