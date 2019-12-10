from os import system

CARDS_PER_LINE = 20


class GUI:
	def __init__(self):
		pass

	def __str__(self):
		system('clear')
		print(self.ascii_version_of_cards(self.in_hand))

	def welcome(self):
		system('clear')
		name = input('\n\n Name: ')
		server = input(' Server: ')
		print(' Connecting to server, think of some clutch strats while you wait..')
		return name, server

	def connected(self):
		# print('waiting in the lobby with..')
		pass

	def update(self, data):
		self.in_hand = data.player_cards[0]
		self.face_up = data.player_cards[1]
		self.face_down = data.player_cards[2]
		self.active = data.discard_cards
		self.message = data.message

	# From https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards
	def ascii_version_of_cards(cards):

		suits_map = {
			'Spades'	: '\u2660',
			'Diamonds'	: '\u2666',
			'Hearts'	: '\u2665',
			'Clubs'		: '\u2663',
			'Red'		: '\u2605',
			'Yellow'	: '\u263e',
			'Green'		: '\u2600',
			'Blue'		: '\u262f',
			'Black'		: '\u263f',
		}

		lines = [[] for i in range(5)]

		for index, card in enumerate(cards):

			if card.value == 'Draw 4':
				rank = '+'
				space = '4'
			elif card.value == 'Draw 2':
				rank = '+'
				space = '2'
			elif card.value == 'Skip':
				rank = 'S'
				space = ' '
			elif card.value == 'Reverse':
				rank = 'R'
				space = ' '
			elif card.value == '10':  # ten is the only one with 2 char long value
				rank = card.value
				space = ''
			else:
				rank = card.value[0]  # some have a rank of 'King' this changes that to a simple 'K'
				space = ' '

			suit = suits_map[card.suit]

			# add the individual card on a line by line basis
			lines[0].append('┌───┐')
			lines[1].append('│{}{} │'.format(rank, space))  # use two {} one for char, one for space or char
			lines[2].append('│ {} │'.format(suit))
			lines[3].append('│ {}{}│'.format(space, rank))
			lines[4].append('└───┘')

		# Not very readable function which prints certain number of cards per line
		for i in range((len(cards) // CARDS_PER_LINE) + 1):
			try:
				for line in lines:
					print('\n'.join([''.join(line[i * CARDS_PER_LINE:(i + 1) * CARDS_PER_LINE])]))
			# for sublime or where can't pretty print cards
			except UnicodeEncodeError:
				for j in cards:
					print(j)
