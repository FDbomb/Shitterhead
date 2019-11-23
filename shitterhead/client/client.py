import socket
from time import sleep

HOST = '192.168.0.5'  # The server's hostname or IP address
PORT = 5555        # The port used by the server


# https://stackoverflow.com/questions/17963485/python-socket-connection-class
class Socket:
	def __init__(self, sock=None):
		self.connected = False
		self.id = None
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

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
			if chunk == b'':
				raise RuntimeError("socket connection broken")
			chunks.append(chunk)
			bytes_recd = bytes_recd + len(chunk)
		return b''.join(chunks)
		'''


self = Socket()

while self.connected is False:
	self.connect(HOST, PORT)

print('Connected')

self.id = self.recv(34).decode()
print(self.id)

while True:
	self.send(f'Yoot from {self.id}'.encode())
	print('Yooted')
	print(self.recv(49).decode())
	sleep(10)
