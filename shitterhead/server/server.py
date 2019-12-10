import concurrent.futures
import json
import logging as log
import socket

from game.game import Game
from common.data import Move, Data


# CONSTANTS #
HOST = '192.168.0.5'
PORT = 5555
PLAYERS = 4


class Client:
	game = None
	clients = []

	def __init__(self, conn, player_id):
		self.id = player_id
		self.player = Client.game.players[self.id]
		self.conn = conn

	# Ensures we read all the data in the buffer for the package
	def recv(self, size):
		recv = ''
		while len(recv) < size:
			temp_recv = self.conn.recv(size - len(recv)).decode()

			if temp_recv != '':
				recv += temp_recv
			else:
				raise BufferError  # If we receive nothing, client has disconnected

		return recv

	# Use this to listen long-term for incoming moves, makes use of custom package format
	def listen_for_moves(self):
		log.info(f'Listening for incoming header from {self.id}')
		header = self.recv(3)
		package_size = int(header)

		log.info(f'Trying to receive package of size {str(package_size)} bytes')
		package = self.recv(package_size)
		log.info(f'Got {len(package)} bytes: {package}')

		return json.loads(package)

	def send(self, data):
		self.conn.sendall(data)

	def send_to_all(self, message=''):
		discard_cards = Client.game.discard_pile.top_playable()
		for client in Client.clients:
			player_cards = client.player.list_hands()
			data = Data(player_cards, discard_cards, message)
			client.send(data.encode())

	def thread(self):
		while self.player.valid_cards() != ([], None):
			try:
				package = self.listen_for_moves()
			except BufferError:  # Except network error, want to shut down thread/connection
				log.warning(f'Player {self.id} disconnected')
				# Client has disconnected so stop trying to send data
				Client.clients = [client for client in Client.clients if client.id != self.id]
				break

			log.info('Handling package')
			move = Move(**package)
			self.player.execute_move(move)

			log.info(f'Sending a yeet out {self.id}')
			self.send_to_all(f'Yeet from server courtesy of {self.id}')

		if Client.game.current_turn != 0:
			# If we have got to this point we have no cards or disconnected from server mid game and
			# so we should be removed from the game
			Client.game.remove_player(self.id)

			# If we remove a client, we sync client.id with player id
			for client in Client.clients:
				client.id = client.player.id

			# Allow player to spectate the rest of the game
			while Client.game.winner is False:
				try:
					# send updates
					pass
				except KeyboardInterrupt:
					break  # Go straight to exit
		else:
			for client in Client.clients:
				if client.id > self.id:
					client.id -= 1
					client.player = Client.game.players[client.id]

		self.id = 99  # Do this so we can easily identify the current client so we can close it
		self.close()  # Remove client and close thread

	def close(self):
		Client.clients = [client for client in Client.clients if client.id != self.id]
		self.conn.close()


def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		with concurrent.futures.ThreadPoolExecutor(max_workers=PLAYERS, thread_name_prefix='Player') as executor:

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
			while len(Client.clients) <= Client.game.no_players - 1:
				conn, addr = s.accept()
				player_id = len(Client.clients)
				log.info(f'{addr} connected as player {player_id}')
				log.info(f'Num of game players: {Client.game.no_players - 1}')

				client = Client(conn, player_id)
				client.send(f'{player_id}'.encode())  # Send player id to new connection
				Client.clients.append(client)
				executor.submit(client.thread)

			log.info('All clients connected...')
