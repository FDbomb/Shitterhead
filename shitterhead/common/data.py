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
	def __init__(self, players_overview, active_players, player_cards, pickup_type, discard_cards=None, active_draw=0, message=None):
		self.players_overview = players_overview
		self.active_players = active_players

		self.player_cards = player_cards

		self.pickup_type = pickup_type
		self.discard_cards = discard_cards
		self.active_draw = active_draw

		self.message = message  # Use this to say 'invalid move, player wins' etc

	def encode(self):
		body = pickle.dumps(self, protocol=pickle.HIGHEST_PROTOCOL)
		header = str(len(body)).zfill(4).encode()
		return header + body

'''
players_overview = {
	0: [no cards, [face_up], [face_down_type]], 
	1: [no cards, [face_up], [face_down_type]]
}
active_players = (current player, reverse=True/False)
player_cards = [
	current active hand for the player
]
pickup_type = uno or playing
discard_cards = top 5 cards + last card is the active card
active_draw = number of cards to pickup
'''

## TO DO ##
#
# Make this only update fields as needed, if player facedown doesn't change dont waste bandwidth