import socket
from _thread import *
# import pickle
# from game import Game

# CONSTANTS #
HOST = '192.168.0.4'
PORT = 5555


def threaded_client(conn, player_id):
	with conn:
		while True:
			data = conn.recv(1024)
			if not data:
				break
			conn.sendall(data)

		print("Lost connection")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

	# Try to start the server
	try:
		s.bind((HOST, PORT))
	except socket.error as e:
		print(str(e))

	s.listen()
	print("Server running, waiting for connection...")

	player_id = 0

	while True:
		conn, addr = s.accept()
		print("Connected to:", addr)
		start_new_thread(threaded_client, (conn, player_id))
		player_id += 1
