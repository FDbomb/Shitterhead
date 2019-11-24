# From client.py to test size of different packet formats, pickle was chosen as smallest file size, easy to encode/decode and standard package

	cards_list = [Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing'), Card('6', 'Hearts', 'playing')]

	xy = Data([cards_list, cards_list, cards_list], cards_list, Move('Play', cards_list).__dict__).__dict__
	xx = Data([cards_list, cards_list, cards_list], cards_list, Move('Play', cards_list), 'Player 2 exiting game after winning')
	print(f'Lenght og cards {len(cards_list)}')
	print('Raw size:', sys.getsizeof(xy))  # === 112
	# print('Json size:', sys.getsizeof(json.dumps(xy)))  # === 180
	print('Pickle size:', sys.getsizeof(pickle.dumps(xx)))

	print('Raw size:', sys.getsizeof(xx))  # === 240
	# print('Json size:', sys.getsizeof(json.dumps(xx)))  # === 182
	print('Pickle size:', sys.getsizeof(pickle.dumps(xx)))  # === 196

	print(xx.encode())
	print('Custom Json size:', sys.getsizeof(xx.encode()))  # === 410

# From data.py, was looking at different package formats

	def Move(action, cards=[]):
		return {
			'action': action,  # Draw, Play, Burn (set by is_valid_move), Pickup (should check no other card is valid), End (set by game)
			'cards': cards
		}


	def Data(player_cards, discard_cards, move, message=None):
		return {
			'player_cards': player_cards,
			'discard_cards': discard_cards,
			'move': move,
			'message': message
		}