# game.py
# main game script, runs the game on the serve
# FDbomb
#
# to do
# - fix burn logic to not burn 5 cards
# - also don't think 4 * 4s will burn in first time of the game, low priority
# - fix play cards for when None is returned from validCards

from collections import deque
import logging as log
from random import shuffle

from common.card import Card
from common.data import Move
# from game.data import Data  # Will be used for network data


FACE_DOWN_CARDS = 3
FACE_UP_CARDS = 3
CARDS_DEALT = 6
CARDS_PER_LINE = 20


class Player:
	def __init__(self, game, player_id):
		self.game = game
		self.id = player_id

		self.face_down = []  # Keeping these as lists to .pop(index)
		self.face_up = []
		self.in_hand = []

		self.picked_up = False  # flag once player has drawn or picked up to block changing faceup cards

	def __str__(self):
		return 'Player ' + str(self.id)

	# takes list of card index from player hand and places them face up
	# note, if a player has less than 6 cards and wishes to change it is impossible
	def addToFacedown(self, cards):

		# accept only if 3 cards are chosen
		if len(cards) == 3 and self.picked_up is False:

			self.in_hand.extend(self.face_up)  # first clear face up cards
			self.face_up = []

			for card in sorted(cards, reverse=True):  # move them in reverse to not change index
				temp = self.in_hand.pop(card)
				self.face_up.append(temp)

			return True
		else:
			return False

	# turn a list of cards into a list of card types, use to hide facedown cards
	def obfuscate_cards(self, cards):
		return [card.type for card in cards]

	# list the hands to send over server, dont want client to know the facedown cards, just their type
	def list_hands(self):
		return [len(self.in_hand), self.face_up, self.obfuscate_cards(self.face_down)]

	# returns the cards that are valid for the player to draw from
	def valid_cards(self):
		# Check if any cards in hand, face up then face down
		if len(self.in_hand) != 0:
			return 'in_hand', self.in_hand
		elif len(self.face_up) != 0:
			return 'face_up', self.face_up
		elif len(self.face_down) != 0:
			return 'face_down', self.face_down

		# we have no cards so we are out, send this to server.py to deal with
		else:
			return None, []

	def execute_move(self, move):
		if move.action == 'Play':
			log.debug(f'1. Playing cards {move.cards}')
			is_valid = self.play_cards(move.cards)
		elif move.action is None:
			is_valid = False  # break early to save some computation, will break for play most cases anyway
		elif move.action == 'Facedown':  # if we are trying to put cards facedown
			try:
				is_valid = self.addToFacedown(move.cards)
			except Exception as e:
				print(e)
		else:
			is_valid = self.draw_cards(move)  # handles Draw and Pickup case

		return is_valid

	def play_cards(self, index):  # make index an array to play multiple cards

		try:  # try to pop selected cards out of player hand
			_, active_hand = self.valid_cards()
			cards = [active_hand.pop(i) for i in sorted(index, reverse=True)]  # Pop indexed cards, need to pop in reverse over to preserve index

		except IndexError:  # if we can't pop cards, we have been given bad index so is_valid is False
			return False

		log.debug(f'2. Cards: {cards}')

		move = Move('Play', cards)
		is_valid, move_return = self.game.do_move(self.id, move)  # do_move will return the card if not valid move, otherwise empty

		# Need to make this return card to same position it was played out of,
		# perhaps if unsuccessful, don't send any card data just say it failed sorry fam
		if len(move_return) > 0:

			for i, ind in enumerate(index):
				self.in_hand[ind:ind] = [move_return[i]]

		log.debug(f'4. Move is {is_valid}')
		return is_valid

	def draw_cards(self, move):  # also handles identical Pickup case
		is_valid, move_return = self.game.do_move(self.id, move)  # do_move will return cards if valid move, otherwise empty
		self.in_hand.extend(move_return)
		return is_valid


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

	def burn(self):
		self.game.burned_pile.add_cards(self.deck)
		self.deck = deque()

	def pick_up(self):
		temp = self.deck
		self.deck = deque()
		return list(temp)

	def top_playable(self):
		active = self.game.active_card
		num_cards = min(5, len(self.deck))  # Chose as many cards as we can up to 5
		top = list(self.deck)[:num_cards]  # Not very efficient :'(

		# We require the active card to be last, if nothing active append ''
		if active == '':  # Try to fix this, annoying to check it each time when it will only happen once per game
			return ['']
		elif active.suit == 'PHANTOM':
			top.append('')  # so append return None if no errors were found, have to return just top
			return top
		else:
			top.append(active)
			return top


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
		self.current_player = -1  # Issue with this is that the next player is counted
		self.reverse = False
		self.winner = False  # Need to periodically update this!!!!!!!!!

		# Current card to play on
		self.active_card = ''
		self.same_active_cards = 0  # Use for burning
		self.active_draw_card = None  # None, draw 2 card, draw 4 card
		self.no_to_draw = 0  # Number of cards to draw

	def remove_player(self, player_id):
		self.no_players -= 1
		del self.players[player_id]

		# If we remove a player, we lower all player numbers higher than the deleted player
		# This allows all the next player logic to continue without issue
		# Could also keep two lists of players, those active and those not
		for player in self.players:
			if player.id > player_id:
				player.id -= 1

	def players_overview(self):
		overview = {}
		for player in self.players:
			overview[player.id] = player.list_hands()
		return overview

	def is_valid_move(self, player, move):

		action = move.action
		cards = move.cards
		is_valid = False

		if player == self.current_player:
			if action == 'Draw':
				# If current draw cards, valid to draw
				if cards == self.no_to_draw:
					is_valid = True

				# Also check that we cannot play anything else so draw won't be a valid move
				playing_from, other_cards = self.players[player].valid_cards()

				# Deal with playing from facedown as a legit move
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

				log.info(f'\nsame active cards: {self.same_active_cards}')
				log.info(f'len cards: {len(cards)}\n')

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
						if len(self.discard_pile.deck) != 0:

							if cards[0].value == self.discard_pile.deck[0].value:
								log.info(f'inn turnn burn, 4 should be {no_cards + self.same_active_cards}')
								if no_cards + self.same_active_cards == 4:
									action = 'Burn'

							# 10 auto burns, easy case
							elif len(cards) == 4 or cards[0].value == '10':
								action = 'Burn'

						elif len(cards) == 4 or cards[0].value == '10':
							action = 'Burn'

				# There is an active draw card
				else:
					if cards[0] >= self.active_draw_card:
						is_valid = True
						# Still want to burn
						if cards[0].value == self.discard_pile.deck[0].value:
							if no_cards + self.same_active_cards == 4:
								action = 'Burn'

			elif action == 'Pickup':

				# cannot pickup if there is a draw card
				if self.active_draw_card is None:

					# otherwise assume pickup is true
					is_valid = True
					active_hand, playable_cards = self.players[player].valid_cards()

					# if we are playing out of face down cards, pickup will always be true
					# however if you can play something else, not valid to pickup
					for card in playable_cards:
						print(f'card: {card.value}')
						_, other_valid = self.is_valid_move(player, Move('Play', [card]))
						print(other_valid)
						if other_valid is True:
							is_valid = False
							break
		else:
			if action == 'Play':

				# Check if we are trying to play more than one card
				if len(cards) > 1:
					# Need to be same value if playing multiple cards
					values = [card.value for card in cards]
					same_cards = len(set(values)) == 1
					if not same_cards:
						# Return straight away if not the same cards
						return action, False

				# Deal with the case when we are playing the first card
				if self.active_card == '':
					log.debug(f'3. Playing on {self.active_card}')

					# Need to be same value if playing multiple cards
					values = [card.value for card in cards]
					log.debug(f'3.1 Values: {values}')
					same_cards = set(values) == set(['4'])  # Check we are playing a 4
					log.debug(f'3.2 Same cards: {same_cards}')
					if same_cards:
						# TO DO: EXPAND THIS IF NO 4s (pretty rare I think)
						# MAKE PEOPLE PICK UP IN ORDER TILL SOMEONE HAS A 4 to play
						# P(No 4s) = C(124/HAND SIZE * NO PLAYERS) / C(132/HAND SIZE * NO PLAYERS) = 0.6%
						is_valid = True

				# Otherwise assume we are trying to burn out of turn
				else:
					if len(self.discard_pile.deck) != 0:
						if cards[0].value == self.discard_pile.deck[0].value:
							if len(cards) + self.same_active_cards == 4:
								log.info('out of turn burnnnnnnn')
								action = 'Burn'
								is_valid = True

		log.info(f'action {action}, valid {is_valid}')
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
				self.players[player].picked_up = True

			# Change key game states
			elif action == 'Play':

				num_cards = len(cards)
				value = cards[0].value

				# Want to check how many of the same cards we have played, and correct count
				# but in case where its an empty deck we look out
				if len(self.discard_pile.deck) > 0:
					if value == self.discard_pile.deck[0].value:
						self.same_active_cards += num_cards
					else:
						self.same_active_cards = num_cards
				else:
					self.same_active_cards = num_cards

				self.discard_pile.add_cards(cards)

				# If we play a 3 we don't want to change anything, it is a pass card
				if value == '3':
					pass

				# Change draw card if playing draw card
				elif value == 'Draw 2' or value == 'Draw 4':
					self.active_draw_card = cards[0]
					self.no_to_draw += int(value[-1:]) * num_cards

				# For each skip card, skip one player
				elif value == 'Skip' or value == 'Queen':
					for i in cards:
						if self.reverse is False:
							self.current_player += 1
						else:
							self.current_player -= 1

					# don't update active card for skip but we need to do it for queen
					if value == 'Queen':
						self.active_card = cards[0]

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
					# if we are playing on the first turn, make current player the person who played the 4
					if self.active_card == '':
						self.current_player = player

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

				# set ourselves as current, then step forward or back
				# so when we step again later it will still be us
				self.current_player = player  # need this for out of turn burns
				if self.reverse is False:
					self.current_player -= 1
				else:
					self.current_player += 1

				# As we burned, return empty list
				cards = []

			elif action == 'Pickup':
				cards = self.discard_pile.pick_up()
				self.active_card = Card('4', 'PHANTOM', 'playing')  # Set a phantom playing card to play on
				self.same_active_cards = 0
				self.players[player].picked_up = True

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

		return is_valid, cards


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
