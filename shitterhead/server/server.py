# server.py
# main script that runs on the server side, handles clients and game
# FDbomb
#
# to do
# - add in command to place face up cards

import concurrent.futures
import json
import logging as log
import socket

from game.game import Game
from common.data import Move, Data


# CONSTANTS #
HOST = '192.168.43.169'  # SET THIS TO YOUR LOCAL IP
PORT = 5555
PLAYERS = 4


class Client:
	game = None
	clients = []
	observers = []

	# self.player points directly to the player object in the game associated with this client instance
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
		header = self.recv(3)  # Header always 3 bytes long
		package_size = int(header)

		log.info(f'Trying to receive package of size {str(package_size)} bytes')
		package = self.recv(package_size)
		log.info(f'Got {len(package)} bytes: {package}')

		return json.loads(package)

	# will send entire package
	def send(self, data):
		self.conn.sendall(data)

	# send all relevant data to all connected clients
	def sendTo(self, clients, observers, message=''):
		discard_cards = Client.game.discard_pile.top_playable()
		players_overview = Client.game.players_overview()
		active_players = (Client.game.current_player, Client.game.reverse)
		pickup_type = Client.game.pickup_deck.deck[0].type
		active_draw = Client.game.no_to_draw

		for i, client in enumerate(clients):

			# returns current playable cards for particular player
			current_hand, player_cards = client.player.valid_cards()

			# if we are playing out of our last hand, need to obfuscate cards
			if current_hand == 'face_down':
				player_cards = ['face_down'] + client.player.obfuscate_cards(player_cards)

			# if we have no cards left, we need to be added to the back of the queue
			elif current_hand is None:

				# remove player from game
				Client.game.remove_player(self.id)

				# make all client ids match the new player ids
				for sub_client in clients:
					if sub_client.id > self.id:
						sub_client.id -= 1

				# also have to step down current player, not sure if this is correct logic though
				if Client.game.current_player > self.id:
					Client.game.current_player -= 1

				Client.observers.append(clients.pop(i))

			data = Data(
				players_overview,
				active_players,
				player_cards,
				pickup_type,
				discard_cards,
				active_draw,
				message
			)

			client.send(data.encode())

		for observer in observers:

			data = Data(
				players_overview,
				active_players,
				[],  # player cards
				pickup_type,
				discard_cards,
				active_draw,
				message
			)

			client.send(data.encode())

		log.debug(f'pickup_type: {pickup_type}\n   discard_cards: {discard_cards}\n   active_draw: {active_draw}')

	def thread(self):
		while self.player.valid_cards() != ([], None):
			try:
				package = self.listen_for_moves()
			except BufferError:  # except network error, want to shut down thread/connection
				log.warning(f'Player {self.id} disconnected')
				# client has disconnected so stop trying to send data
				Client.clients = [client for client in Client.clients if client.id != self.id]
				break

			log.info('Handling package')
			move = Move(**package)
			was_valid = self.player.execute_move(move)

			try:
				if was_valid is True:
					log.info('Sending package to all')
					self.sendTo(Client.clients, Client.observers, f'Yeet from server courtesy of {self.id}')
				else:
					log.info(f'Sending package to {self.id}')
					# need to wrap self in a list here as we try to iterate over it
					self.sendTo([self], [], f'Yeet from server courtesy of {self.id}')
			except Exception as e:
				print(e)

		if Client.game.current_turn != 0:
			# if we have got to this point we have no cards or disconnected from server mid game and
			# so we should be removed from the game
			Client.game.remove_player(self.id)

			# if we remove a client, we sync client.id with player id
			for client in Client.clients:
				client.id = client.player.id

			# allow player to spectate the rest of the game
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

		self.id = 99  # do this so we can easily identify the current client so we can close it
		self.close()  # remove client and close thread

	def close(self):
		Client.clients = [client for client in Client.clients if client.id != self.id]
		self.conn.close()


def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		with concurrent.futures.ThreadPoolExecutor(max_workers=PLAYERS, thread_name_prefix='Player') as executor:

			log.info('Starting Game...')
			Client.game = Game(PLAYERS)

			# try to start the server
			try:
				s.bind((HOST, PORT))
			except socket.error as e:
				print(str(e))
				exit()

			# listen for connections
			s.listen()
			log.info("Server running, waiting for connection...")

			# connect players
			while len(Client.clients) <= Client.game.no_players - 1:
				conn, addr = s.accept()
				player_id = len(Client.clients)
				log.info(f'{addr} connected as player {player_id}')
				log.info(f'Num of game players: {Client.game.no_players - 1}')

				client = Client(conn, player_id)
				client.send(f'{player_id}'.encode())  # send player id to new connection
				Client.clients.append(client)
				executor.submit(client.thread)

			log.info('All clients connected...')
			# send out map of player id and player names
