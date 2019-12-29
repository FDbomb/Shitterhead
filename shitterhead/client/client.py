import concurrent.futures
import logging as log
import pickle
from time import sleep

from client.GUI import GUI
from client.socket import Socket
from common.data import Move, Data

log.basicConfig(format='%(asctime)s - %(filename)s - %(threadName)s - %(message)s', datefmt='%H:%M:%S', level=log.DEBUG)


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
			self.gui.conn_failed()

	def socket_thread(self):
		while True:
			try:
				data = self.socket.listen_for_data()
				data = pickle.loads(data)
				# update_gui(data)
				print(data.message)
			except BufferError:
				log.info('Server shutdown')
				break

	def gui_thread(self):
		# Put printing code here,
		# keyboard listening,
		# and other fun stuff
		data = Move('Play', [1])
		self.socket.send(data.encode())
		log.info('Sent play')
		sleep(10)

	def main_thread(self):

		with concurrent.futures.ThreadPoolExecutor(max_workers=1, thread_name_prefix='Recv Thread') as executor:
			sock_thread = executor.submit(self.socket_thread)

			while sock_thread.running():
				self.gui_thread()

		self.socket.send(''.encode())  # Properly close the socket here
		log.warning('Client shutdown')


def main():

	client = Client()
	client.main_thread()


if __name__ == '__main__':
	main()
