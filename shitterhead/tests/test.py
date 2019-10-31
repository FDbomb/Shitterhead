from game.game import *


# Helper Functions #
def set_up():
	g = Game(3)

	return g


def print_decks(g):

	for i in g.players:
		print(i, ':')
		ascii_version_of_cards(i.in_hand)

	print('Pickup Deck :')
	ascii_version_of_cards(g.pickup_deck.deck)

	print('Discard pile :')
	ascii_version_of_cards(g.discard_pile.deck)

	print('Burned Cards :')
	ascii_version_of_cards(g.burned_pile.deck)


# Test Functions #
def test_inital_decks(g):
	print(len(g.pickup_deck))
	print(len(g.players[0].in_hand))
	print(len(g.discard_pile))

	print("\n\n\n")

	ascii_version_of_cards(g.players[0].in_hand)

	print("\n\n\n")

	g.players[0].play_card(0)
	ascii_version_of_cards(g.discard_pile.deck)

	print("\n\n\n")

	ascii_version_of_cards(g.players[0].in_hand)

	print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

	for i in g.discard_pile.deck:
		print(i)

	print("\n\n\n")

	for i in g.pickup_deck.deck:
		print(i)


def burning_and_reinject(g):
	g.players[0].play_card(0)

	print_decks(g)

	g.discard_pile.burn()
	g.burned_pile.re_inject()

	print_decks(g)


def main():

	g = set_up()
	test_inital_decks(g)
	burning_and_reinject(g)


if __name__ == '__main__':
	main()
