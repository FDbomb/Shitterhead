from tests import gameplay, server
from client import client


def run():
	# Run gameplay tests
	gameplay.main()

	# Run server tests
	server.main()


def receive():
	# Run as a client instead
	client.main()
