import json
import logging as log
import pickle
import socket
from time import sleep

import sys
sys.path.append("..")
from Shitterhead.shitterhead.common.data import Move, Data
from Shitterhead.shitterhead.common.card import Card

# CONSTANTS #
HOST = '192.168.0.5'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

log.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)


# https://stackoverflow.com/questions/17963485/python-socket-connection-class
class Socket:
	def __init__(self):
		self.connected = False
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.id = None
		self.player = None

	def connect(self, host, port):
		self.sock.connect((host, port))
		self.connected = True

	def send(self, msg):
		self.sock.sendall(msg)

	def recv(self, size):
		return self.sock.recv(size)

		'''
		chunks = []
		bytes_recd = 0
		while bytes_recd < 1024:
			chunk = self.sock.recv(min(1024 - bytes_recd, 2048))
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return b''.join(chunks)'''


def main():
	self = Socket()

	while self.connected is False:
		self.connect(HOST, PORT)
	log.info('Connected')

	self.id = self.recv(34).decode()
	log.info(f'Set as player {self.id}')

	while True:
		data = Move('Play', [1, 3])
		self.send(data.encode())
		log.info('Yooted')
		log.info(self.recv(49).decode())
		sleep(10)


if __name__ == '__main__':
	main()
