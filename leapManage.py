# -*- coding: utf-8 -*-


#################################################################
# Leap Motion with nao
# Bachelor thesis

# Descritpion: Class LeapManage
# Author:      Niels Jacot
# Date:        12.07.2013
##################################################################


#local import
import constante

#import
import Leap, sys
import time
from Leap import SwipeGesture
from PyQt4 import QtCore



FORWARD = 1.0
BACKWARD = -1.0
RIGHT = -1.0
LEFT = 1.0



class LeapManage(Leap.Listener, QtCore.QThread):
	#Class used to manage all the move that's receive from the Leap
	
	def __init__(self, naoMotion, deviceControl, parent = None):
		# Constructor
		
		Leap.Listener.__init__(self)
		QtCore.QThread.__init__(self, parent)
		
		self.parent = parent
		self.naoMotion = naoMotion
		self.alive = 1
		self.deviceControl = deviceControl
		self.currentMode = constante.INIT_MODE
		self.currentSide = constante.RIGHT_HAND
		self.cptHello = 0
		self.walk = False
		self.forward = True
		self.controller = Leap.Controller()
		self.controller.set_policy_flags(1) # enable background application
		
		
	def on_init(self, controller):
		print "Initialized"

	def on_connect(self, controller):
		print "Connected"

		# Enable swipe gestures
		self.controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

	def on_disconnect(self, controller):
		# Note: not dispatched when running in a debugger.
		print "Disconnected"

	def on_exit(self, controller):
		print "Exited"

	def on_frame(self, controller):
		# Get the most recent frame and report some basic information
		frame = controller.frame()
		frame2 = controller.frame(5)

		if not frame.hands.empty:
			# Get the first hand
			hand = frame.hands[0]

			# Check if the hand has any fingers
			fingers = hand.fingers

			# Get the hand's normal vector and direction
			normal = hand.palm_normal
			direction = hand.direction
			palmPosx = hand.palm_position.x
			palmPosy = hand.palm_position.y
			palmPosz = hand.palm_position.z
			
			if self.testBox(palmPosx, palmPosy, palmPosz):
				if len(fingers) == 5:
					self.getHandSide(fingers)
			
			#Test in wich mode we are
			if self.currentMode == constante.WALK_MODE:
				self.walk = True
				self.walkNao(direction, palmPosx)
			elif self.currentMode == constante.INIT_MODE:
				self.naoMotion.stopWalk(constante.FREQUENCY)
				self.walk = False
				self.initNao(frame)
			elif self.currentMode == constante.HEAD_MODE:
				self.naoMotion.stopWalk(constante.FREQUENCY)
				self.walk = False
				self.moveHead(direction, palmPosx, palmPosy, palmPosz)
			elif self.currentMode == constante.ARM_MODE:
				self.naoMotion.stopWalk(constante.FREQUENCY)
				self.walk = False
				hand2 = frame.hands[1]
				if len(frame.hands) == 2 or len(frame2.hands) == 2:
					self.moveTwoArms(frame, hand, hand2)
				else:
					self.moveArm(palmPosx,palmPosy,palmPosz,normal.roll)
			elif self.currentMode == constante.HAND_MODE:
				self.naoMotion.stopWalk(constante.FREQUENCY)
				self.walk = False
				self.closeOpenHand(fingers)
		
		if not (frame.hands.empty and frame.gestures().empty):
			print"."
			
	def testWalkOnOff(self):
		if self.walk == False:
			self.naoMotion.stopWalk(constante.FREQUENCY)
			
	def closeOpenHand(self, fingers):
		if not fingers.empty:
			self.naoMotion.openHand(self.currentSide)
		else:
			self.naoMotion.closeHand(self.currentSide)
			
	def testBox(self, palmPosx, palmPosy, palmPosz):
		if -40 < palmPosx < 40 and 100 < palmPosy < 200 and -40 < palmPosz < 40: return True	
		else:
			return False
			
	def initNao(self, frame):
		for gesture in frame.gestures():
				if gesture.type == Leap.Gesture.TYPE_SWIPE:
					swipe = SwipeGesture(gesture)
					
					#direction of a swipe is equal to 1 if it goes up and -1 for down
					if swipe.direction.y > 0.97 and swipe.speed > 1500.0: 
						self.naoMotion.standInit()
					elif swipe.direction.y < -0.97  and swipe.speed > 1000.0:
						self.naoMotion.crouch()
						
					# helloBoy: mvt lateral
					elif -0.03 < swipe.direction.y < 0.03 and swipe.speed > 1000:
						self.cptHello += 1
						if self.cptHello < 2:
							self.naoMotion.runHello()
						else:
							self.cptHello = 0
					
	def walkNao(self, direction, palmPosx):
		if self.walk:
			if self.deviceControl.sensorConnected:
				values = self.deviceControl.sensorManage.getFeetSensor()
				
				# Stop if there is a contact on a bumper
				if 1.0 in values:
					self.forward = False
					self.naoMotion.stop()
					self.naoMotion.tts.say("Attention, faites demi tours tout de suite")
					
				else:
					if direction.pitch * Leap.RAD_TO_DEG > 45  and self.forward:
						print"avance"
						self.naoMotion.walk(FORWARD,0.0,0.0,constante.FREQUENCY)		
					elif direction.pitch * Leap.RAD_TO_DEG <-40:
						print"recule"
						self.naoMotion.walk(BACKWARD,0.0,0.0,constante.FREQUENCY)
						self.forward = True
					elif palmPosx > 180:
						print"droite"
						self.naoMotion.walk(0.0,RIGHT,0.0,constante.FREQUENCY)
					elif palmPosx < -180:
						print"gauche"
						self.naoMotion.walk(0.0,LEFT,0.0,constante.FREQUENCY)
					elif -30 < direction.pitch * Leap.RAD_TO_DEG < 30 and direction.yaw * Leap.RAD_TO_DEG > 35:
						self.naoMotion.walk(0.0,0.0,-0.5,constante.FREQUENCY)
					elif -30 < direction.pitch * Leap.RAD_TO_DEG < 30 and direction.yaw * Leap.RAD_TO_DEG < -35:
						self.naoMotion.walk(0.0,0.0,0.5,constante.FREQUENCY)
					else:
						self.naoMotion.stopWalk(constante.FREQUENCY)
						
		else:
			self.naoMotion.stop()
			
	def moveArm(self, palmPosx, palmPosy,palmPosz,normal):
		self.naoMotion.moveArm(palmPosx, palmPosy, palmPosz, normal, self.currentSide)
			
	def moveTwoArms(self, frame, hand, hand2):
		listPos = []
		
		if hand == frame.hands.leftmost:	
			palmPosLeftX = hand.palm_position.x
			listPos.append(palmPosLeftX)
			palmPosLeftY = hand.palm_position.y
			listPos.append(palmPosLeftY)
			palmPosLeftZ = hand.palm_position.z
			listPos.append(palmPosLeftZ)
			normalLeft = hand.palm_normal.roll
			listPos.append(normalLeft)
			
			palmPosRightX = hand2.palm_position.x
			listPos.append(palmPosRightX)
			palmPosRightY = hand2.palm_position.y
			listPos.append(palmPosRightY)
			palmPosRightZ = hand2.palm_position.z
			listPos.append(palmPosRightZ)
			normalRight = hand2.palm_normal.roll
			listPos.append(normalRight)
			
		else:
			palmPosLeftX = hand2.palm_position.x
			listPos.append(palmPosLeftX)
			palmPosLeftY = hand2.palm_position.y
			listPos.append(palmPosLeftY)
			palmPosLeftZ = hand2.palm_position.z
			listPos.append(palmPosLeftZ)
			normalLeft = hand2.palm_normal.roll
			listPos.append(normalLeft)
			
			palmPosRightX = hand.palm_position.x
			listPos.append(palmPosRightX)
			palmPosRightY = hand.palm_position.y
			listPos.append(palmPosRightY)
			palmPosRightZ = hand.palm_position.z
			listPos.append(palmPosRightZ)
			normalRight = hand.palm_normal.roll
			listPos.append(normalRight)
	
		self.naoMotion.naoMoveTwoArms(listPos)
			
			
	def moveHead(self, direction, palmPosx, palmPosy, palmPosz):
		if -40 < palmPosx < 40 and 100 < palmPosy < 350 and -40 < palmPosz < 40:
			angles  = [-direction.yaw, -direction.pitch]
			self.naoMotion.moveHead(angles)
		
	def getHandSide(self, fingers):
		if fingers.rightmost.length > fingers.leftmost.length and fingers.leftmost.direction.roll < 0 and fingers.leftmost.direction.cross(fingers.rightmost.direction).y < 0:					
			self.currentSide = constante.RIGHT_HAND
		elif fingers.leftmost.length > fingers.rightmost.length and fingers.rightmost.direction.roll > 0 and fingers.rightmost.direction.cross(fingers.leftmost.direction).y > 0:
			self.currentSide = constante.LEFT_HAND	

	def state_string(self, state):
		if state == Leap.Gesture.STATE_START:
			return "STATE_START"

		if state == Leap.Gesture.STATE_UPDATE:
			return "STATE_UPDATE"

		if state == Leap.Gesture.STATE_STOP:
			return "STATE_STOP"

		if state == Leap.Gesture.STATE_INVALID:
			return "STATE_INVALID"	
		
	def run(self):
		while self.alive:
			# Have the sample listener receive events from the controller
			self.controller.add_listener(self)
		
	def stopLeap(self):
		print"StopLeap"
		
		self.alive = 0
		#self.terminate()
		
	def __del__(self):
		self.wait()