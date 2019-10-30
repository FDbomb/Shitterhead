#from network import Network
# import pickle


#def main():
#	n = Network()
#	player = n.send("hello")
#	print(player)


#main()

import socket

HOST = '192.168.0.4'  # The server's hostname or IP address
PORT = 5555        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		s.sendall(b'Hello, world')
		data = s.recv(1024)
		print('Received', repr(data))
