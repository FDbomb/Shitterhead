import logging
from random import shuffle
from collections import deque

from game.card import Card
from common.data import Move, Data
# from game.data import Data  # Will be used for network data

# CONTSTANTS #
FACE_DOWN_CARDS = 3
FACE_UP_CARDS = 3
CARDS_DEALT = 15  # NEED TO FIX THIS - CAN BUMP DECK SIZE OR DYNAMICALLY CHANGE THIS

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
CARDS_PER_LINE = 20


# CLASSES #
class Player:
	def __init__(self, game, player_id):
		self.game = game
		self.id = player_id

		self.face_down = []  # Keeping these as lists to .pop(index)
		self.face_up = []
		self.in_hand = []

	def __str__(self):
		return 'Player ' + str(self.id)

	def pickle_into_data(self):
		pass

	def unpickle_update_player(self):
		# if move is play card
		# then self.play
		# if move is pickup, then self.pickup
		pass

	# Returns the cards that are valid for the player to draw from
	def valid_cards(self):
		# Check if any cards in hand, face up then face down
		if len(self.in_hand) != 0:
			return 'in_hand', self.in_hand
		elif len(self.face_up) != 0:
			return 'face_up', self.face_up
		elif len(self.face_down) != 0:
			return 'face_down', self.face_down
		# We should have won at this point
		else:
			return []

	def play_cards(self, index):  # make index an array to play multiple cards
		cards = [self.in_hand.pop(i) for i in sorted(index, reverse=True)]  # Pop indexed cards, need to pop in reverse over to preserve index
		action = Move('Play', cards)
		move_return = self.game.do_move(self.id, action)  # do_move will return the card if not valid move, otherwise empty

		# Need to make this return card to same position it was played out of,
		# perhaps if unsuccessful, don't send any card data just say it failed sorry fam
		if len(move_return) > 0:
			for i in index:
				self.in_hand[i:i] = [move_return[i]]

	def draw_cards(self, no_cards):
		action = Move('Draw', no_cards)
		move_return = self.game.do_move(self.id, action)  # do_move will return cards if valid move, otherwise empty
		self.in_hand.extend(move_return)

	def pickup(self, no_cards):
		action = Move('Draw', no_cards)
		move_return = self.game.do_move(self.id, action)  # do_move will return cards if valid move, otherwise empty
		self.in_hand.extend(move_return)


class Deck:
	def __init__(self, game):
		self.game = game
		self.deck = deque()

	def __len__(self):
		return len(self.deck)

	def print_deck(self):
		for i in self.deck:
			print(i)

	def add_cards(self, cards=[]):
		self.deck.extendleft(cards)


class PickupDeck(Deck):
	def __init__(self, game):
		Deck.__init__(self, game)

		# Create deck of playing cards
		for i in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
			for j in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']:
				to_append = [Card(j, i, 'playing')] * 2
				self.add_cards(to_append)

		# Generate coloured UNO CARDS
		for i in ['Red', 'Yellow', 'Green', 'Blue']:
			for j in ['Skip', 'Reverse', "Draw 2"]:
				to_append = [Card(j, i, 'uno')] * 2
				self.add_cards(to_append)

		# Generate Draw 4 cards
		for i in range(4):
			self.add_cards([Card('Draw 4', 'Black', 'uno')])

		# Shuffle pickup deck
		shuffle(self.deck)

	def give_top_cards(self, n):
		# Recursively try to give top card, not sure
		# if this is the best idea as will just loop forever
		# if we run out of cards, rather than throw an error.
		# Very exteme case to break it, not sure if even possible to
		# get into such a situation
		cards = []
		for i in range(n):
			try:
				cards.append(self.deck.popleft())
			except IndexError:
				self.game.burned_pile.reinject()
				cards.append(self.give_top_cards(1))
		return cards

	def deal_helper(self, const, deck):
		for i in range(const * self.game.no_players):
			temp = self.give_top_cards(1)
			getattr(self.game.players[i % self.game.no_players], deck).extend(temp)
		del temp

	def deal_cards(self):

		# Deal facedown cards
		self.game.pickup_deck.deal_helper(FACE_DOWN_CARDS, 'face_down')

		# Deal player cards
		self.game.pickup_deck.deal_helper(CARDS_DEALT, 'in_hand')


class DiscardPile(Deck):
	def __init__(self, game):
		Deck.__init__(self, game)

	def four_of_a_kind(self):
		return

	def burn(self):
		self.game.burned_pile.add_cards(self.deck)
		self.deck = deque()

	def pick_up(self, player_id):
		temp = self.deck
		self.deck = Deck()
		return list(temp)


class BurnedPile(Deck):
	def __init__(self, game):
		Deck.__init__(self, game)

	def re_inject(self):
		shuffle(self.deck)
		self.game.pickup_deck.deck = self.deck
		self.deck = deque()


class Game:
	def __init__(self, no_players):

		# Create pickup deck and discard pile
		self.pickup_deck = PickupDeck(self)
		self.discard_pile = DiscardPile(self)
		self.burned_pile = BurnedPile(self)

		# Create player hands
		self.no_players = no_players  # Always >= 2
		self.players = []
		for i in range(self.no_players):
			self.players.append(Player(self, i))

		# Deal cards to players and pickup pile
		self.pickup_deck.deal_cards()

		# Store various game states
		self.current_turn = 0
		self.current_player = -1
		self.reverse = False
		self.winner = False  # Need to periodically update this!!!!!!!!!

		# Current card to play on
		self.active_card = ''
		self.same_active_cards = 0  # Use for burning
		self.active_draw_card = None  # None, draw 2 card, draw 4 card
		self.no_to_draw = 0  # Number of cards to draw

	def is_valid_move(self, player, move):

		action = move.action
		cards = move.cards
		is_valid = False

		if player == self.current_player:
			if action == 'Draw':
				# If current draw cards, valid to draw
				if cards == self.no_to_draw:
					is_valid = True

				# Also check if we can play something so draw won't be a valid move
				playing_from, other_cards = self.players[player].valid_cards()

				if playing_from != 'face_down':
					for card in other_cards:
						_, other_valid = self.is_valid_move(player, Move('Play', [card]))
						if other_valid:
							is_valid = False
							break
				# Insert gambling logic here
				else:
					pass

			elif action == 'Play':

				no_cards = len(cards)
				# Check if we are trying to play more than one card
				if no_cards > 1:
					# Need to be same value if playing multiple cards
					values = [card.value for card in cards]
					same_cards = len(set(values)) == 1
					if not same_cards:
						# Return straight away if not the same cards
						return action, False

				# Normal gameplay
				if self.active_draw_card is None:
					# This takes into account power cards: 6 >= 7 is True, Draw 4 >= Draw 2 == False
					if cards[0] >= self.active_card:
						is_valid = True
						# Check for burns
						if cards[0].value == self.active_card.value:
							if no_cards + self.same_active_cards == 4:
								action = 'Burn'
							elif no_cards + self.same_active_cards > 4:  # If you try to burn with too many, fix this later
								is_valid = False
						elif cards[0].value == '10':
							action = 'Burn'

				# There is an active draw card
				else:
					if cards[0] >= self.active_draw_card:
						is_valid = True
						# Still want to burn
						if no_cards + self.same_active_cards == 4:
							action = 'Burn'
						elif no_cards + self.same_active_cards > 4:
							is_valid = False

			elif action == 'Pickup':
				# Assume pickup is true
				is_valid = True
				# However if you can play something else, not valid to pickup
				for card in self.player_in_hand(player):
					_, other_valid = self.is_valid_move(player, Move('Play', card))
					if other_valid:
						is_valid = False
						break
		else:
			if action == 'Play':

				# Deal with the case when we are playing the first card
				if self.active_card == '':
					# If we are here we know both cards have same value so just take first card
					if cards[0].value == 4:
						# TO DO: EXPAND THIS IF NO 4s (pretty rare I think)
						# P(No 4s) = C(124/HAND SIZE * NO PLAYERS) / C(132/HAND SIZE * NO PLAYERS) = 0.6%
						is_valid = True

				# Otherwise assume we are trying to burn out of turn
				else:
					if cards[0].value == self.active_card.value:
						if len(cards) + self.same_active_cards == 4:
							action = 'Burn'
							is_valid = True

		return action, is_valid

	def do_move(self, player, move):
		# This method should always return a list

		action, is_valid = self.is_valid_move(player, move)
		cards = move.cards

		if is_valid:
			# If we are drawing, pop top cards off pickup and return them
			# to let the player deal with putting them in their hand
			if action == 'Draw':
				cards = self.pickup_deck.give_top_cards(cards)
				self.active_draw_card = None
				self.no_to_draw = 0

			# Change key game states
			elif action == 'Play':
				value = cards[0].value

				# Want to check how many of the same cards we have played, and correct count
				# but in case where its an empty deck we look out
				if len(self.discard_pile.deck) > 0:
					if value == self.discard_pile.deck[0].value:
						self.same_active_cards += len(cards)
					else:
						self.same_active_cards = len(cards)

				self.discard_pile.add_cards(cards)

				# If we play a 3 we don't want to change anything, it is a pass card
				if value == '3':
					pass

				# Change draw card if playing draw card
				elif value == 'Draw 2' or value == 'Draw 4':
					self.active_draw_card = cards[0]
					self.no_to_draw += int(value[-1:])

				# For each skip card, skip one player
				elif value == 'Skip' or value == 'Queen':
					for i in cards:
						if self.reverse is False:
							self.current_player += 1
						else:
							self.current_player -= 1

				# For each reverse card, toggle self.reverse
				elif value == 'Reverse':
					# If we are down to 2 players, treat reverse as skip
					if self.no_players == 2:
						self.current_player += 1  # Only two players so don't care about direction
					# Otherwise play it as normal
					else:
						for i in cards:
							self.reverse = not self.reverse

				# Change active card if playing card, include 7 and 2 in here (10 will go to burn)
				elif cards[0].type == 'playing':
					self.active_card = cards[0]

				# We want to return empty list as we successfully played the cards
				cards = []

			elif action == 'Burn':
				self.discard_pile.add_cards(cards)
				self.discard_pile.burn()
				self.active_card = Card('4', 'PHANTOM', 'playing')  # Anything can be played on this
				self.same_active_cards = 0
				self.active_draw_card = None
				self.no_to_draw = 0

				# We go back one player, so when we step forward below we will end up back at ourselves
				if self.reverse is False:
					self.current_player -= 1
				else:
					self.current_player += 1

				# As we burned, return empty list
				cards = []

			elif action == 'Pickup':
				cards = self.pickup_deck.pick_up()
				self.active_card = Card('4', 'PHANTOM', 'playing')  # Set a phantom playing card to play on
				self.same_active_cards = 0

			# Change current player and current turn
			self.current_turn += 1
			if self.reverse is False:
				self.current_player = (self.current_player + 1) % self.no_players
			else:
				self.current_player = (self.current_player - 1) % self.no_players

		else:
			# If we unsuccessfully tried to draw, return nothing
			if action == 'Draw':
				cards = []

		return cards


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
			space = ' '  # no "10", we use a blank space to will the void

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
