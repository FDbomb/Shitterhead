import json
import pickle


# Used in Game, Date, and sent from client to server
class Move:
	def __init__(self, action=None, cards=[]):
		self.action = action  # Draw, Play, Burn (set by is_valid_move), Pickup (should check no other card is valid), End (set by game)
		self.cards = cards

	def encode(self):
		body = json.dumps(self.__dict__, separators=(',', ':')).encode()
		header = str(len(body)).zfill(3).encode()
		return header + body


# Sent from server to client
class Data:
	def __init__(self, player_cards=None, discard_cards=None, message=None):
		self.player_cards = player_cards
		self.discard_cards = discard_cards
		self.message = message  # Use this to say 'invalid move, player wins' etc

	def encode(self):
		body = pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
		header = str(len(body)).zfill(4).encode()
		return header + body
