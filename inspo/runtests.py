import unittest
from test_card import TestCard
from test_player import TestPlayer
from test_deck import TestDeck
from test_game import TestGame

test_cases = ["test_card",
              "test_player",
              "test_deck",
              "test_game"]

suite = unittest.TestLoader().loadTestsFromNames(test_cases)
unittest.TextTestRunner(verbosity=2).run(suite)
