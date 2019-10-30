class Card:
	def __init__(self, val, suit, kind):
		self.value = val
		self.suit = suit  # includes colour for UNO cards
		self.type = kind  # uno or playing

	# Allows us to print(Card)
	def __str__(self):
		if self.type == 'uno':
			return self.suit + ' ' + self.value
		else:
			return self.value + ' of ' + self.suit

	def __lt__(self, other_card):
		if self.type == 'uno' or self.value == 3:
			return True
		else:
			return self.value < other_card.value

	def __le__(self, other_card):
		if self.type == 'uno' or self.value == 3:
			return True
		else:
			return self.value <= other_card.value

	def __eq__(self, other_card):
		return self.value == other_card.value

	def __ne__(self, other_card):
		return self.value != other_card.value

	def __gt__(self, other_card):
		if self.type == 'uno' or self.value == 3:
			return True
		else:
			return self.value > other_card.value

	def __ge__(self, other_card):
		if self.type == 'uno' or self.value == 3:
			return True
		else:
			return self.value >= other_card.value
