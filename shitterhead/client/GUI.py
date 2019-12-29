from os import system

from client import fonts

CARDS_PER_LINE = 20


class GUI:
	def __init__(self):
		pass

	# Append a small face up card
	def small_fu(self, lines, value, space=''):

		# Pad out cards with rank only 1 char long
		if len(value) == 1:
			space = ' '

		lines[1].append('┌──┐')
		lines[2].append('│{}{}│'.format(space, value))
		lines[3].append('└──┘')
		return lines

	# Append a small face down card that is under a face up card
	def half_fd(self, lines, card_type):
		lines[1].append('─┐ ')
		lines[2].append('{}│ '.format(card_type))  # type of card, U or P
		lines[3].append('─┘ ')
		return lines

	# Append a small face down card by itself
	def small_fd(self, lines, card_type):
		lines[1].append('┌──┐ ')
		lines[2].append('│░{}│ '.format(card_type))  # type of card, U or P
		lines[3].append('└──┘ ')
		return lines

	def player_overview(self, name, data, current):
		# Most of this is defined in the data.py file
		no_cards = data[0]
		face_up = [card.value for card in data[1]]
		face_down = data[2]

		# 4 lines per player, name on 1st line and card for next 3 lines
		lines = [[] for _ in range(4)]

		# Current is the current player (**) or next player ( *) or none (  )
		lines[0].append('{}  {}: {}'.format(current, name, no_cards))

		# If we have faceup cards
		if len(face_up) != 0:
			i = 0
			# We print all face up and half fd cards to match
			while i < len(face_up):
				lines = self.small_fu(lines, face_up[i].value)
				lines = self.half_fd(lines, face_down[i].type)
				i += 1
			# If we run out of face up cards, we print the remaining fd cards
			while i < 3:
				lines = self.small_fd(lines, face_down[i].type)
				i += 1
		# If no face up cards, we just print all available facedown cards
		else:
			for card_type in face_down:
				lines = self.small_fd(lines, card_type)

		return '\n'.join([''.join(line) for line in lines])

	def __str__(self, data):
		system('clear')
		print(fonts.gameplay_title)

		# Calculate current and next player, based on if we are reversed or not
		curr_player = data.active_players[0]
		if data.active_players[1] is False:
			direction = 1
		else:
			direction = -1
		next_player = (curr_player + direction) % len(data.players_overview)

		# Loop through players to print the little overviews
		for player, data in self.players_overview.items():
			# Use status to highlight current and next players
			if player == curr_player:
				status = '**'
			elif player == next_player:
				status = '* '
			else:
				status = ' '

			# Print the little overview for each player
			print(self.player_overview(player, data, status))

		print('')
		print(self.ascii_version_of_cards(self.in_hand))

	def welcome(self):
		system('clear')
		print(fonts.welcome_title)

		name = input('\n\n Name: ')
		while len(name) > 20:
			system('clear')
			print('\n\n That\'s a pretty fucking long name, anything shorter I can call you...')
			input(' Name: ')

		server = input(' Server: ')
		print(' Connecting to server, think of some clutch strats while you wait..')
		return name, server

	def connected(self):
		print(' Connection successful')

	def conn_failed(self):
		print(' Connection refused, please check server address and try again')

	def update_cards(self, data):
		self.players_overview = data.players_overview

		self.player_cards = data.player_cards

		self.pickup_type = data.pickup_type
		self.discard_cards = data.discard_cards
		self.active_draw = data.active_draw

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

		lines = [[] for _ in range(5)]

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
