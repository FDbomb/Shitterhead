# GUI.py
# module to handle printing GUI and receiving player commands
# FDbomb
#
# to do
# - fix case where player has more cards than can be displayed in one line
# - - can either make scrollable with command or add second line
# - fix current/next player showing on game start
# - make more beautiful
# - eventually move off command line


from os import system
from client import fonts


CARDS_PER_LINE = 20
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


class GUI:
	def __init__(self):
		pass

	def welcome(self):
		system('cls||clear')
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
		print(' Connection successful, press enter to continue')

	def connFailed(self):
		print(' Connection refused, please check server address and try again')

	def updateStates(self, data):
		self.players_overview = data.players_overview

		# calculate current and next player, based on if we are reversed or not
		self.curr_player = data.active_players[0]
		if data.active_players[1] is False:
			direction = 1
		else:
			direction = -1
		self.next_player = (self.curr_player + direction) % len(self.players_overview)

		self.player_cards = data.player_cards

		self.pickup_type = data.pickup_type
		self.discard_cards = data.discard_cards
		self.active_draw = data.active_draw

		self.message = data.message

	# given a card value, this returns a shorter 2 char value
	def shortCardValues(self, value):

		if value == 'Draw 4':
			value = '+'
			space = '4'
		elif value == 'Draw 2':
			value = '+'
			space = '2'
		elif value == 'Skip':
			value = 'S'
			space = ' '
		elif value == 'Reverse':
			value = 'R'
			space = ' '
		elif value == '10':  # ten is the only one with 2 char long value
			space = ''
		else:
			value = value[0]  # some have a rank of 'King' this changes that to a simple 'K'
			space = ' '

		return space, value

	# append a small face up card
	def smallFU(self, lines, value):

		space, value = self.shortCardValues(value)

		lines[1].append('┌──┐')
		lines[2].append('│{}{}│'.format(space, value))
		lines[3].append('└──┘')
		return lines

	# append a small face down card that is under a face up card
	def smallHalfFD(self, lines, card_type):
		lines[1].append('─┐ ')
		lines[2].append('{}│ '.format(card_type[0].upper()))  # type of card, U or P
		lines[3].append('─┘ ')
		return lines

	# append a small face down card by itself
	def smallFD(self, lines, card_type):
		lines[1].append('┌──┐ ')
		lines[2].append('│░{}│ '.format(card_type[0].upper()))  # first letter of type of card, U or P
		lines[3].append('└──┘ ')
		return lines

	def bigFU(self, lines, space, value, suit):

		lines[0].append(' ┌───┐')
		lines[1].append(' │{}{} │'.format(value, space))  # use two {} one for char, one for space or char
		lines[2].append(' │ {} │'.format(suit))
		lines[3].append(' │ {}{}│'.format(space, value))
		lines[4].append(' └───┘')

		return lines

	def bigHalfFU(self, lines, space, value, suit):

		lines[0].append('───┐')
		lines[1].append('{}{} │'.format(value, space))  # use two {} one for char, one for space or char
		lines[2].append(' {} │'.format(suit))
		lines[3].append(' {}{}│'.format(space, value))
		lines[4].append('───┘')

		return lines

	def bigFD(self, lines, card_type):

		lines[0].append('┌───┐ ')
		lines[1].append('│░░░│ ')
		lines[2].append('│░{}░│ '.format(card_type[0].upper()))
		lines[3].append('│░░░│ ')
		lines[4].append('└───┘ ')

		return lines

	def showPlayersOverview(self, name, data, current):
		# most of this is defined in the data.py file
		no_cards = data[0]
		face_up = [card.value for card in data[1]]  # list of values as strings
		face_down = data[2]  # list of types (uno or playing) as strings

		# 4 lines per player, name on 1st line and card for next 3 lines
		lines = [[] for _ in range(4)]

		# current is the current player (**) or next player ( *) or none (  )
		lines[0].append('{}  {}: {}'.format(current, name, no_cards))

		# if we have faceup cards
		if len(face_up) != 0:
			i = 0
			# we print all face up and half fd cards to match
			while i < len(face_up):
				lines = self.smallFU(lines, face_up[i])
				lines = self.smallHalfFD(lines, face_down[i])
				i += 1
			# if we run out of face up cards, we print the remaining fd cards
			while i < 3:
				lines = self.smallFD(lines, face_down[i])
				i += 1
		# if no face up cards, we just print all available facedown cards
		else:
			for card_type in face_down:
				lines = self.smallFD(lines, card_type)

		return '\n'.join([''.join(line) for line in lines])

	def activeCards(self):

		lines = [[] for _ in range(5)]  # big cards are 5 lines

		# print pickup deck
		lines = self.bigFD(lines, self.pickup_type)

		# add some buffer space to visually seperate pickup and discard pile
		for line in lines:
			line.append('  ')

		# the active card will always be the last card
		# if no active cards will be empty string, active_card = ''
		active_card = self.discard_cards.pop()

		# print the top playable cards
		for index, card in enumerate(self.discard_cards):

			space, value = self.shortCardValues(card.value)
			suit = suits_map[card.suit]

			# print top card seperately as it is a full face up card
			# and then each successive card as a half face up card
			if index == 0:
				lines = self.bigFU(lines, space, value, suit)
			else:
				lines = self.bigHalfFU(lines, space, value, suit)

		# add on active draw cards and active play card
		if self.active_draw != 0:
			lines[1].append(f'  To pickup: {self.active_draw}')

		if active_card != '':
			temp = self.smallFU(['_', lines[2], lines[3], lines[4]], active_card.value)
			_, lines[2], lines[3], lines[4] = temp  # this needs more testing

		return '\n'.join([''.join(line) for line in lines])

	# from https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards
	def inHandCards(self):

		cards = self.player_cards
		lines = [[] for _ in range(6)]  # big cards are 5 lines + 1 line for index

		# if we are working with face down cards, we must not show the cards
		if cards[0] == 'face_down':

			for index, card_type in enumerate(cards[1:]):
				lines = self.bigFD(lines, card_type)
				lines[5].append(' [{:02d}] '.format(index))

		# otherwise we can show face up cards
		else:
			for index, card in enumerate(cards):

				space, value = self.shortCardValues(card.value)
				suit = suits_map[card.suit]

				# add face up cards and their corresponding index below
				lines = self.bigFU(lines, space, value, suit)
				lines[5].append(' [{:02d}] '.format(index))

		# not very readable function which prints certain number of cards per line
		for i in range((len(cards) // CARDS_PER_LINE) + 1):
			try:
				return '\n'.join([''.join(line[i * CARDS_PER_LINE:(i + 1) * CARDS_PER_LINE]) for line in lines])
			# for sublime or where can't pretty print cards
			except UnicodeEncodeError:
				return 'rip cannot print cards for some reason, tell Felix he is a derro'

	def refresh(self):
		system('cls||clear')
		print(fonts.gameplay_title)

		# loop through players to print the little overviews
		for player, data in self.players_overview.items():
			# use status to highlight current and next players
			if player == self.curr_player:
				status = '**'
			elif player == self.next_player:
				status = '* '
			else:
				status = '  '

			try:
				# print the little overview for each player
				print(self.showPlayersOverview(player, data, status) + '\n')
			except Exception as e:
				print(e)

		# print active playing cards
		try:
			print(self.activeCards())
		except Exception as e:
			print(e)

		# print your own cards
		print(self.inHandCards())

		# print input colons
		print('\n:: ', end='')  # for some reason we need \n here, idk
