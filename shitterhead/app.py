import logging

from tests import gameplay, server
from client import client

logging.basicConfig(format='%(asctime)s - %(filename)s - %(threadName)s - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


def run():
	# Run gameplay tests
	gameplay.main()

	# Run server tests
	server.main()


def receive():
	# Run as a client instead
	client.main()
