class Card:
	mapping = {'4': 0, '5': 1, '6': 2, '7': 3, '8': 4, '9': 5, 'Jack': 6, 'Queen': 7, 'King': 8, 'Ace': 9}

	def __init__(self, value, suit, kind):
		self.value = value
		self.suit = suit  # includes colour for UNO cards
		self.type = kind  # uno or playing

	# Allows us to print(Card)
	def __str__(self):
		if self.type == 'uno':
			return self.suit + ' ' + self.value
		else:
			return self.value + ' of ' + self.suit

	def __ge__(self, other_card):
		val = self.value
		comp_val = other_card.value

		if val == '3':
			return True

		elif val == 'Draw 2':
			if comp_val == 'Draw 4':
				return False
			else:
				return True

		elif val == 'Draw 4':
			if comp_val == 'Draw 2':
				return False
			else:
				return True

		elif val == '2' or val == '10' or self.type == 'uno':
			if comp_val == 'Draw 4' or comp_val == 'Draw 2':
				return False
			else:
				return True

		else:
			if comp_val == 'Draw 2' or comp_val == 'Draw 4':
				return False
			elif comp_val == '7':
				return self.mapping[val] <= self.mapping[comp_val]
			else:
				return self.mapping[val] >= self.mapping[comp_val]
