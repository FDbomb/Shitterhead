import concurrent.futures
import logging as log
import socket
from time import sleep

from game.game import Game
from common.data import Move, Data


# CONSTANTS #
HOST = '192.168.0.5'
PORT = 5555
PLAYERS = 4


class Client:
	game = None

	def __init__(self, conn, player_id):
		self.id = player_id
		self.conn = conn

	def receive(self, size):
		return self.conn.recv(size)

	def send(self, data):
		self.conn.sendall(data)

	def close(self):
		self.conn.close()


def threaded_client(self):
	while True:

		log.info(f'Listening for incoming header from {self.id}') # noqa
		package_size = self.receive(4).decode()
		log.info(f'Trying to receive package of size {package_size}b')
		package = self.receive(int(package_size)).decode()
		print('Got package:', package)
		log.info(f'Sending a yeet back to {self.id}')
		self.send(b'Yeet from server')

		log.info(f'For client {self.id} current turn is {self.game.current_turn}')
		self.game.current_turn = 10


def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		clients = []  # How to get rid of this, very useless
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		with concurrent.futures.ThreadPoolExecutor(max_workers=PLAYERS) as executor:

			log.info('Starting Game...')
			Client.game = Game(PLAYERS)

			# Try to start the server
			try:
				s.bind((HOST, PORT))
			except socket.error as e:
				print(str(e))
				exit()

			# Listen for connections
			s.listen()
			log.info("Server running, waiting for connection...")

			# Connect players
			player_id = 0
			while player_id <= PLAYERS - 1:
				conn, addr = s.accept()
				log.info(f'{addr} connected as player {player_id}')

				client = Client(conn, player_id)
				client.send(f'{player_id}'.encode())  # Send player id to new connection
				executor.submit(threaded_client, client)
				clients.append(client)

				
				player_id += 1

			log.info('All clients connected...')
