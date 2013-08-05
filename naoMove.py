# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class NaoMove
# Author:      Niels Jacot
# Date:        12.07.2013
#################################################################



# local import 
import constante

#import
import sys
from naoqi import ALProxy

# Some constante used in this class
ANGLE_MAX = 1.5
ANGLE_MIN = -1.5

MAXPOSX = 120

SHOULDERROLL = 0
SHOULDERPITCH = 1
ELBOWROLL = 2
WRISTYAW = 3


class NaoMove():
	# Class used to make all movements to Nao
	def __init__(self, parent):
		#Constructor
		
		self.motionProxy = None
		self.postureProxy = None
		self.tts = None
		self.memoryProxy = None
		self.behaviourProxy = None
		
		self.motorOn = False
		self.parent = parent
		
		self.memValue = ["FaceDetected"]
		
		self.headNames = ["HeadYaw", "HeadPitch"]
		self.leftArmNames = ["LShoulderRoll","LShoulderPitch","LElbowRoll","LElbowYaw"]
		self.rightArmNames = ["RShoulderRoll","RShoulderPitch","RElbowRoll","RElbowYaw"]
		
	def connect(self, robotIP, port):
		try:
			self.motionProxy = ALProxy("ALMotion", robotIP , port)
			self.tts = ALProxy("ALTextToSpeech", robotIP, port)
			self.postureProxy = ALProxy("ALRobotPosture", robotIP, port)
			self.memoryProxy = ALProxy("ALMemory", robotIP, port)
			self.behaviourProxy = ALProxy("ALBehaviorManager", robotIP, port)
		except:
			return 1
			
		# If connection is successful, we initialize few variables for Arms	
		self.anglesRight = self.motionProxy.getAngles(self.rightArmNames, True)
		self.anglesLeft = self.motionProxy.getAngles(self.leftArmNames, True)
		return 0
		
		
	def walk(self,x,y,theta,frequency):
		# Test if the stiffness of Nao is set to 1.0
		self.testMotorOn()
		
		# Launch the walk
		self.motionProxy.setWalkTargetVelocity(x, y, theta, frequency)
		
	def stopWalk(self, frequency):
		self.motionProxy.setWalkTargetVelocity(0.0, 0.0, 0.0, frequency)
		self.motionProxy.waitUntilMoveIsFinished()
		
	def stop(self):
		self.motionProxy.killMove()
		
	def standInit(self):
		self.postureProxy.goToPosture("StandInit", constante.FREQUENCY)
		
	def crouch(self):
		self.postureProxy.goToPosture("Crouch", constante.FREQUENCY)
		
	def runHello(self):
		self.testMotorOn()
		
		self.behaviourProxy.runBehavior("helloBoy")
		
	def openHand(self, hand):
		if hand == constante.RIGHT_HAND:
			self.motionProxy.openHand('RHand')
		else:
			self.motionProxy.openHand('LHand')
	
	def closeHand(self, hand):
		if hand == constante.RIGHT_HAND:
			self.motionProxy.closeHand('RHand')
		else:
			self.motionProxy.closeHand('LHand')
			
	def moveHead(self, angles):
		# Test if the stiffness of Nao is set to 1.0
		self.testMotorOn()
		
		current = self.motionProxy.getAngles(self.headNames, True)
		
		# this boucle is used to dynamically calculate the speed of the movement
		for i in range(len(angles)):
			speed = abs(angles[i]-current[i])/2.0
			
			if speed < 0.05:
				speed = 0.05
			if speed > 0.8:
				speed = 0.8
				
			# Make the movement
			self.motionProxy.setAngles(self.headNames[i], angles[i], speed)
			
	def detectFace(self):
		# Check that it is not already running.
		if (not self.behaviourProxy.isBehaviorRunning("faceDetect")):
			# Launch behavior. This is a blocking call, use post if you do not
			# want to wait for the behavior to finish.
			self.behaviourProxy.post.runBehavior("faceDetect")
		
	def naoMoveTwoArms(self, listPos):
		# Test if the stiffness of Nao is set to 1.0
		self.testMotorOn()
		
		if self.setCollisionEnabled("RArm") and self.setCollisionEnabled("LArm"):
			current = self.motionProxy.getAngles(self.rightArmNames, True)
			angles = self.anglesRight
			
			current2 = self.motionProxy.getAngles(self.leftArmNames, True)
			angles2 = self.anglesLeft
			two = True
			
			self.processMoveArm(angles2, current2, listPos[0], listPos[1], listPos[2], listPos[3], 0,two)
			self.processMoveArm(angles, current, listPos[4], listPos[5], listPos[6], listPos[7], 1, two)
			
	def moveArm(self, palmPosx, palmPosy, palmPosz, normal, handSide):
		# Test if the stiffness of Nao is set to 1.0
		self.testMotorOn()
		two = False
			
		if self.setCollisionEnabled("RArm") and self.setCollisionEnabled("LArm"):
			if handSide == constante.RIGHT_HAND:
				current = self.motionProxy.getAngles(self.rightArmNames, True)
				angles = self.anglesRight
			elif handSide == constante.LEFT_HAND:
				current = self.motionProxy.getAngles(self.leftArmNames, True)
				angles = self.anglesLeft
				
			self.processMoveArm(angles, current, palmPosx, palmPosy, palmPosz, normal, handSide, two)
			
	def processMoveArm(self, angles, current, palmPosx, palmPosy, palmPosz, normal, handSide, two):
		# If there is two arms, the values of the box are not the same 
		if two:
			maxPosLeftx = -100
			minPosLeftx = -180
			maxPosRightx = 180
			minPosRightx = 100
		else:
			maxPosLeftx = MAXPOSX
			minPosLeftx = -MAXPOSX
			maxPosRightx = MAXPOSX
			minPosRightx = -MAXPOSX
			
		if handSide == constante.RIGHT_HAND:
			#ElbowRoll
			self.setAngleRight(angles, ELBOWROLL, 0.0, 1.5, 75, -40, palmPosz)
			
			#ShoulderRoll
			if palmPosx > maxPosRightx:
				if angles[0] <= -1.5:
					angles[0] = -1.5
				angles[0] -= 0.1
			elif palmPosx < minPosRightx:
				if angles[0] >= 0.0:
					angles[0] = 0.0
				angles[0] += 0.1
			
		else:
			#handSide = left
			
			#ShoulderRoll
			if palmPosx > maxPosLeftx:
				if angles[0] >= 1.5:
					angles[0] = 1.5
				angles[0] -= 0.1
			elif palmPosx < minPosLeftx:
				if angles[0] <= 0.0:
					angles[0] = 0.0
				angles[0] += 0.1
				
			#ElbowRoll
			self.setAngleLeft(angles, ELBOWROLL, -1.5, 0.0, 75, -40, palmPosz)
			
		#ShoulderPitch	
		self.setAngleLeft(angles, SHOULDERPITCH, -1.5, 1.5, 350, 150, palmPosy)
		
		if 0.78 > normal > -0.78:
			angles[3] = -normal
			
		for i in range(len(angles)):
			speed = abs(angles[i]-current[i])/2.0
			if speed < 0.05:
				speed = 0.05
			if speed > 0.5:
				speed = 0.5
				
			name = self.rightArmNames[i]
			if handSide == constante.LEFT_HAND:
				name = self.leftArmNames[i]
				
			# Make the movement
			self.motionProxy.setAngles(name, angles[i], speed)
	
	def setAngleRight(self, angles, indice, valueMin, valueMax, posMax, posMin, palmPos):
		if palmPos > posMax:
			if angles[indice] >= valueMax:
				angles[indice] = valueMax
			angles[indice]+= 0.1
		elif palmPos < posMin:
			if angles[indice] <= valueMin:
				angles[indice] = valueMin
			angles[indice] -= 0.1
		
	def setAngleLeft(self, angles, indice, valueMin, valueMax, posMax, posMin, palmPos):
		if palmPos > posMax:
			if angles[indice] <= valueMin:
				angles[indice] = valueMin
			angles[indice] -= 0.1
		elif palmPos < posMin:
			if angles[indice] >= valueMax:
				angles[indice] = valueMax
			angles[indice] += 0.1
						
	def setCollisionEnabled(self, chainName):
		#activate "Arms" anticollision
		enable    = True
		isSuccess  = self.motionProxy.setCollisionProtectionEnabled(chainName, enable)
		return isSuccess	
				
	def turnMotorOn(self):
		#Turn on the nao's motors
		names  = 'Body'
		stiffnessLists  = 1.0
		timeLists  = 1.0
		self.motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
		self.motorOn = True
		
	def testMotorOn(self):
		if not self.motorOn:
			self.turnMotorOn()
			
	def stiffnessOff(self):
		names  = 'Body'
		stiffnessLists  = 0.0
		timeLists  = 1.0
		self.motionProxy.stiffnessInterpolation(names, stiffnessLists, timeLists)
		self.motorOn = False
		
		self.behaviourProxy.stopAllBehaviors()
		
	
	
	
		
		
	