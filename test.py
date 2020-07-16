import asyncio
import serial_asyncio
import time
import numpy as np

from mavfleetcontrol.craft import Craft
from mavfleetcontrol.actions.point import FlyToPoint
from mavfleetcontrol.actions.percision_land import PercisionLand
from mavfleetcontrol.actions.arm import Arm
from mavfleetcontrol.actions.disarm import Disarm
from mavfleetcontrol.actions.land import land
from mavfleetcontrol.actions.circle import Circle




class Output(asyncio.Protocol):
	def connection_made(self, transport):
		self.transport = transport
		print('port opened', transport)
		transport.serial.rts = False
		transport.write(b'hello world\n')

	def data_received(self, msg):
		# print('data received', repr(data))
		try:
			if(msg==b'.'):
			# heartbeat(drone)
				pass
			if(((msg)[:2])==(b'OA')):
			# print((msg)[2])
				if(((msg)[2])==49):
					drone.add_action(Arm())
				if(((msg)[2])==50):
					drone.add_action(Disarm())
				if(((msg)[2])==51):
					drone.add_action(FlyToPoint(np.array([0, 0, -1]), tolerance=2.5))
				if(((msg)[2])==52):
					drone.add_action(land())
				if(((msg)[2])==53):
					drone.add_action( PercisionLand( 1.0,   np.array([1, 1])   )  )
				if(((msg)[2])==54):
					drone.add_action(FlyToPoint(np.array([0,0,-10]),tolerance =1))
				if(((msg)[2])==55):
					drone.add_action(Circle(velocity=20.0,radius=8.0,angle=0.0))
				if(((msg)[2])==57):
					drone.override_action(Spin())
				if(((msg)[2])==57):
					drone.override_action(Killing())
		except Exception as E:
			print(E)
	def connection_lost(self, exc):
		print('port closed')
		asyncio.get_event_loop().stop()

# drone = Craft("drone1","serial:///dev/serial0:1000000")
drone = Craft('drone0',"udp://:14540")
drone.start()
loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyUSB1', baudrate=57600)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()