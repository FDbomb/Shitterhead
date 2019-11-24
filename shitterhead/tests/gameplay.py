from common.card import Card
from game.game import Game, ascii_version_of_cards


# Helper Functions #
def set_up():
	g = Game(3)

	return g


def print_decks(g):

	print('\n')
	for i in g.players:
		print(i, ':')
		ascii_version_of_cards(i.in_hand)

	print('\nPickup Deck :')
	ascii_version_of_cards(g.pickup_deck.deck)

	print('\nDiscard pile :')
	ascii_version_of_cards(g.discard_pile.deck)

	print('\nBurned Cards :')
	ascii_version_of_cards(g.burned_pile.deck)


# Test Functions #
def test_random_shuffle(g):

	print('\n')
	print('# in pickup  :', len(g.pickup_deck))
	print('# in player0 :', len(g.players[0].in_hand))
	print('# in discard :', len(g.discard_pile))

	print('\n\n')
	print('Player 0 hand')
	ascii_version_of_cards(g.players[0].in_hand)

	print('\n\n..Changing game states, adding 4 and player 0 turn now..')
	g.active_card = Card('4', 'Hearts', 'playing')
	g.current_player = 0

	print('..Now playing card 0 (for player 0)..')
	g.players[0].play_cards([0])

	print('\n\nDiscard pile (should be old card 0)')
	ascii_version_of_cards(g.discard_pile.deck)

	print('\n\n')
	print('Player 0 hand now (should be down 1 card')
	ascii_version_of_cards(g.players[0].in_hand)

	print('\n\n')
	print('Discard pile:')
	for i in g.discard_pile.deck:
		print('		', i)

	print('\n\n')
	print('Pickup Deck:')
	for i in g.pickup_deck.deck:
		print('		', i)


def test_burn_reinject(g):

	print('\n\n')
	print('\n..Again playing card 0 (for player 0)..\n')
	g.players[0].play_cards([0])

	print_decks(g)

	print('\n..Burning the discard_pile and filling the pickup with burned cards..\n')
	g.discard_pile.burn()
	g.burned_pile.re_inject()

	print_decks(g)


def test_power_cards(g):

	print('\n\n..Changing game states, adding 4 and player 0 turn now..')
	g.active_card = Card('4', 'Hearts', 'playing')
	g.current_player = 0

	print('\n\n..Initialise player 0s hand')
	g.players[0].in_hand = [
		# Play 5
		Card('5', 'Hearts', 'playing'),
		# Play 7 on 7
		Card('7', 'Hearts', 'playing'),
		Card('7', 'Hearts', 'playing'),
		# Burn with four 6
		Card('6', 'Hearts', 'playing'),
		Card('6', 'Hearts', 'playing'),
		Card('6', 'Hearts', 'playing'),
		Card('6', 'Hearts', 'playing'),
		# Play 4
		Card('4', 'Hearts', 'playing'),
		# Skip and reverse
		Card('Skip', 'Red', 'uno'),
		Card('Reverse', 'Red', 'uno'),
		# Stack Draw 2
		Card('Draw 2', 'Red', 'uno'),
		Card('3', 'Hearts', 'playing'),
		Card('Draw 2', 'Red', 'uno'),
		# Pickup 4
	]
	ascii_version_of_cards(g.players[0].in_hand)

	print('\n\n..Playing 5, [7, 7], [6, 6, 6]')
	g.players[0].play_cards([0])
	g.current_player = 0
	g.players[0].play_cards([0, 1])
	g.current_player = 0
	g.players[0].play_cards([0, 1, 2])
	print('\n Player 0:')
	ascii_version_of_cards(g.players[0].in_hand)
	print('Discard pile:')
	ascii_version_of_cards(g.discard_pile.deck)

	print('\n\n..Playing 6 (out of turn), 4')
	for i in range(2):
		g.players[0].play_cards([0])
		g.current_player = 0
	print('\n Player 0:')
	ascii_version_of_cards(g.players[0].in_hand)
	print('Discard pile:')
	ascii_version_of_cards(g.discard_pile.deck)
	print('Burned pile:')
	ascii_version_of_cards(g.burned_pile.deck)

	print('\n\n..Playing Skip and Reverse')
	for i in range(2):
		print('Playing:', g.players[0].in_hand[0].value, end=' == ')
		g.players[0].play_cards([0])
		print('Current player:', g.current_player)
		g.current_player = 0
	print('\n Player 0:')
	ascii_version_of_cards(g.players[0].in_hand)
	print('Discard pile:')
	ascii_version_of_cards(g.discard_pile.deck)
	print('Burned pile:')
	ascii_version_of_cards(g.burned_pile.deck)

	print('\n\n..Playing Draw 2, 3, Draw 2')
	for i in range(3):
		g.players[0].play_cards([0])
		g.current_player = 0
	print('\n Player 0:')
	ascii_version_of_cards(g.players[0].in_hand)
	print('Discard pile:')
	ascii_version_of_cards(g.discard_pile.deck)
	print('Burned pile:')
	ascii_version_of_cards(g.burned_pile.deck)

	print('\n\n..Drawing 4 cards')
	g.players[0].draw_cards(4)
	print('\n Player 0:')
	print('In hand')
	ascii_version_of_cards(g.players[0].in_hand)
	print('Face down')
	ascii_version_of_cards(g.players[0].face_down)
	print('Discard pile:')
	ascii_version_of_cards(g.discard_pile.deck)
	print('Burned pile:')
	ascii_version_of_cards(g.burned_pile.deck)


def main():

	'''
	g = set_up()
	test_random_shuffle(g)
	test_burn_reinject(g)
	'''

	g = set_up()
	test_power_cards(g)


if __name__ == '__main__':
	main()
