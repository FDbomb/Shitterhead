class Action:
	def __init__(self, action, card=None):
		self.action = action  # Draw, Play, Burn, End (turn)
		self.card = card
