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
from sys import exit

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

	# given a user input, this will return the input as a Move(action, list from user input)
	def inputToMove(self, action, string):

		str_cards = '[' + string + ']'  # convert input into string list

		# try to eval sting list into valid list
		try:
			cards = list(literal_eval(str_cards))
			assert(any(isinstance(x, int) for x in cards))
		# if we can't convert to a valid list, we start again
		except (AssertionError, SyntaxError, ValueError):
			print('Not a valid command, try again you derelict')
			return self.getInput()

		return Move(action, cards)

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
			# select which cards to play facedown
			elif command[0] == 'F':
				try:
					data = self.inputToMove('Facedown', command[1:])  # strip the leading F
				except Exception as e:
					print(e)
			# otherwise assume it is a list of cards to play
			else:
				data = self.inputToMove('Play', command)

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
				log.debug('Server shutdown')
				print('Server has shut down, press enter to exit')
				exit()

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

		try:  # try to properly close the socket here, probably will get pipe error
			self.socket.send(''.encode())
		except BrokenPipeError:
			pass  # just catch the error to avoid printing to terminal


def main():

	client = Client()
	client.mainThread()


if __name__ == '__main__':
	main()
