import json
import pickle
from sys import getsizeof


# Used in Game and in Date
class Move:
	def __init__(self, action, cards=[]):
		self.action = action  # Draw, Play, Burn (set by is_valid_move), Pickup (should check no other card is valid), End (set by game)
		self.cards = cards

	def encode(self):
		body = json.dumps(self.__dict__, separators=(',', ':')).encode()
		header = str(getsizeof(body)).zfill(4).encode()
		return header + body


# Sent between client and server
class Data:
	def __init__(self, player_cards=None, discard_cards=None, move=None, message=None):
		# self.id = str(player_id)  # Not sure if this is needed, wanted to check the data came from the right place
		self.player_cards = player_cards
		self.discard_cards = discard_cards
		self.move = move
		self.message = message  # Use this to say 'invalid move, player wins' etc

	def encode(self):
		body = pickle.dumps(self)
		header = str(getsizeof(body)).zfill(4)
		return header + body
