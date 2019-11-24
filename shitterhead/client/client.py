import concurrent.futures
import json
import logging as log
import pickle
import socket
from time import sleep

from common.data import Move, Data

# CONSTANTS #
HOST = '192.168.0.7'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

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

		self.id = self.recv(1)  # Can hang here, need to fix this but close to zero chance of that happening
		log.info(f'Connected as player {self.id}')

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

	def pkl_recv(self, size):
		recv = b''
		while len(recv) < size:
			temp_recv = self.sock.recv(size - len(recv))

			if temp_recv != '':
				recv += temp_recv
			else:
				raise BufferError  # If we receive nothing, server has disconnected

		return recv

	def listen_for_data(self):
		log.info(f'Listening for incoming header from server')
		header = self.recv(4)
		package_size = int(header)

		log.info(f'Trying to receive package of size {str(package_size)} bytes')
		package = self.pkl_recv(package_size)
		log.info(f'Got all {len(package)} bytes')

		return package

	def thread(self):
		while True:
			try:
				data = self.listen_for_data()
				data = pickle.loads(data)
				log.info(data.message)
			except BufferError:
				log.info('Server shutdown')
				break


def main():
	self = Socket()

	while self.connected is False:
		self.connect(HOST, PORT)

	with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='Recv Thread') as executor:
		recv_thread = executor.submit(self.thread)

		while recv_thread.running():
			data = Move('Play', [1])
			self.send(data.encode())
			log.info('Sent play')
			sleep(10)

	self.send(''.encode())  # Properly close the socket here
	log.warning('Client shutdown')


if __name__ == '__main__':
	main()
