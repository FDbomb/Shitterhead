from random import shuffle
from collections import deque

from game.card import Card
from game.data import Data

# https://www.mixcloud.com/PAUL_DI/alison-wonderland-on-mix-up-triple-j-jjj-09022017/

# CONTSTANTS #
FACE_DOWN_CARDS = 3
FACE_UP_CARDS = 3
CARDS_DEALT = 15  # NEED TO FIX THIS - CAN BUMP DECK SIZE OR DYNAMICALLY CHANGE THIS

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

	def play_card(self, index):  # make index an array to play multiple cards, or card instead of index, return first match?
		self.game.discard_pile.add_card(self.in_hand.pop(index))


class Deck:
	def __init__(self, game):
		self.game = game
		self.deck = deque()

	def __len__(self):
		return len(self.deck)

	def print_deck(self):
		for i in self.deck:
			print(i)

	def add_card(self, card):
		self.deck.append(card)

	def remove_top_card(self):
		return self.deck.popleft()


class PickupDeck(Deck):
	def __init__(self, game):
		Deck.__init__(self, game)

		# Create deck of playing cards
		for i in ['Hearts', 'Diamonds', 'Spades', 'Clubs']:
			for j in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']:
				to_append = [Card(j, i, 'playing')] * 2
				self.deck.extend(to_append)

		# Generate coloured UNO CARDS
		for i in ['Red', 'Yellow', 'Green', 'Blue']:
			for j in ['Skip', 'Reverse', "Draw 2"]:
				to_append = [Card(j, i, 'uno')] * 2
				self.deck.extend(to_append)
		# Generate Draw 4 cards
		for i in range(4):
			self.deck.append(Card('Draw 4', 'Black', 'uno'))

		# Shuffle pickup deck
		shuffle(self.deck)

	def deal_helper(self, const, deck):
		for i in range(const * self.game.no_players):
			temp = self.remove_top_card()
			getattr(self.game.players[i % self.game.no_players], deck).append(temp)
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
		self.game.burned_pile.deck.extend(self.deck)
		self.deck = deque()

	def pick_up_deck(self, player_id):
		self.game.players[player_id].in_hand.extend(self.game.pickup_deck)
		self.deck = Deck()


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

		# Store various game states
		self.current_turn = 0
		self.current_player = -1
		self.actions_this_turn = 0
		self.next_player = self.current_player + 1  # Hmm, might cause some bugs but useful for skip

		# Current card to play on
		self.active_card = ''
		self.active_draw_cards = ''

	def player_no_cards(self, player_id, deck):
		return len(getattr(self.players[player_id], deck))

	def player_n_hand(self, player_id):
		no_in_hand = self.player_no_cards(player_id, 'in_hand')
		no_face_up = self.player_no_cards(player_id, 'face_up')
		no_face_down = self.player_no_cards(player_id, 'face_up')

		if no_in_hand != 0:
			return self.players[player_id].in_hand
		elif no_face_up != 0:
			return self.players[player_id].face_up
		elif no_face_down != 0:
			return self.players[player_id].face_down
		else:
			return 'PLayer id win!!!!!!!!!'


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


# MAIN #
def main():
	g = Game(3)
	g.pickup_deck.deal_cards()


if __name__ == '__main__':
		main()
