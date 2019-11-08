# Used in Game and in Date
class Move:
	def __init__(self, action, cards=[]):
		self.action = action  # Draw, Play, Burn (set by is_valid_move), Pickup (should check no other card is valid), End (set by game)
		self.cards = cards


# Sent between client and server
class Data:
	def __init__(self, player_cards, discard_cards, move, message):
		self.player_cards = player_cards
		self.discard_cards = discard_cards
		self.move = move
		self.message = message
