import logging as log
import socket
from time import sleep


# https://stackoverflow.com/questions/17963485/python-socket-connection-class
class Socket:
	def __init__(self):
		self.id = None  # Player id
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False

	def connect(self, server):
		self.host = '127.0.0.1'  # CHANGE THIS TO SERVER ADDRESS!!!!
		self.port = 5555

		con_attempts = 0
		while self.connected is False and con_attempts < 60:
			try:
				self.sock.connect((self.host, self.port))
				self.connected = True

				self.id = self.recv(1)  # Can hang here, need to fix this but close to zero chance of that happening
				print(f' Connected as player {self.id}')

			except (ConnectionRefusedError, OSError):
				con_attempts = 1
				sleep(1)
				print(' Trying again')

	def send(self, msg):
		self.sock.sendall(msg)

	def recv(self, size):
		recv = ''
		while len(recv) < size:
			temp_recv = self.sock.recv(size - len(recv)).decode()

			if temp_recv != '':
				recv += temp_recv
			else:
				raise BufferError  # If we receive nothing, client has disconnected

		return recv

	def recvPkl(self, size):
		recv = b''
		while len(recv) < size:
			temp_recv = self.sock.recv(size - len(recv))

			if temp_recv != '':
				recv += temp_recv
			else:
				raise BufferError  # If we receive nothing, server has disconnected

		return recv

	def listenForData(self):
		log.debug(f'Listening for incoming header from server')
		header = self.recv(4)
		package_size = int(header)

		log.debug(f'Trying to receive package of size {str(package_size)} bytes')
		package = self.recvPkl(package_size)
		log.debug(f'Got all {len(package)} bytes')

		return package
