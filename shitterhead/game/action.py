class Action:
	def __init__(self, action, card=None):
		self.action = action  # Draw, Play, Burn (set by is_valid_move), End (turn)
		self.cards = cards
