# client.py
# main client script, handles interaction between socket, GUI, and player input
# FDbomb
#
# to do
# - pickup command is broken, P and no cards were added

from ast import literal_eval
import concurrent.futures
import logging as log
import pickle

from client.GUI import GUI
from client.socket import Socket
from common.data import Move, Data


class Client:
	def __init__(self):
		self.gui = GUI()
		self.socket = Socket()

		self.name, server = self.gui.welcome()

		# Try to connect, if no connection after 1 min we exit with an error message
		self.socket.connect(server)

		if self.socket.connected is True:
			self.gui.connected()
		else:
			self.gui.connFailed()

	# will return a Move() given a valid user input, or None if no valid move
	def getInput(self):
		# get user input, :: printed by GUI thread already
		command = input('')
		data = None

		# first check command isn't empty
		if command != '':
			# draw cards
			if command[0] == 'D':
				data = Move('Draw', self.gui.active_draw)
			# pickup discard pile
			elif command[0] == 'P':
				data = Move('Pickup')
			# otherwise assume it is a list of cards
			else:
				command = '[' + command + ']'  # convert input into list
				# try to convert it to a valid list
				try:
					cards = list(literal_eval(command))
					assert(any(isinstance(x, int) for x in cards))
					data = Move('Play', cards)
				# if we can't convert to a valid list, we start again
				except (AssertionError, SyntaxError, ValueError):
					print('Not a valid command, try again you derelict')
					return self.getInput()

		return data

	def socketThread(self):
		while True:
			try:
				# Listen for data (of type Data), and unpickle it
				data = self.socket.listenForData()
				data = pickle.loads(data)

				# Update gui states and show this new state
				self.gui.updateStates(data)
				self.gui.refresh()

			# If we experience an error listening for data, we know the server has shutdown as so we should exit
			except BufferError:
				log.info('Server shutdown')
				break

	def guiThread(self):

		data = self.getInput()

		# send move if we have data
		if data is not None:
			self.socket.send(data.encode())
			log.debug('Sent play')
		# if we have no data, send out null will only cost 26 bytes
		else:
			self.socket.send(Move().encode())

	def mainThread(self):

		with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='Recv Thread') as executor:
			sock_thread = executor.submit(self.socketThread)

			while sock_thread.running():
				self.guiThread()

		self.socket.send(''.encode())  # Properly close the socket here
		log.warning('Client shutdown')


def main():

	client = Client()
	client.mainThread()


if __name__ == '__main__':
	main()
