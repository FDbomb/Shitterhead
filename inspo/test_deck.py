from deck import Deck
from card import Card
import unittest

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck(52)
        self.two = Card(2, 1)
        self.three = Card(3, 1)
        self.four = Card(4, 1)
        self.five = Card(5, 1)
        self.six = Card(6, 1)
        self.seven = Card(7, 1)
        self.eight = Card(8, 1)
        self.nine = Card(9, 1)
        self.ten = Card(10, 1)
        self.jack = Card(11, 1)
        self.queen = Card(12, 1)
        self.king = Card(13, 1)
        self.ace = Card(14, 1)        
    
    def test_create_0_cards(self):
        deck = Deck(0)
        self.assertEqual(len(deck), 0)

    def test_create_20_cards(self):
        deck = Deck(20)
        self.assertEqual(len(deck), 52)
    
    def test_create_51_cards(self):
        deck = Deck(51)
        self.assertEqual(len(deck), 52)

    def test_create_52_cards(self):
        deck = Deck(52)
        self.assertEqual(len(deck), 52)
        
    def test_create_53_cards(self):
        deck = Deck(53)
        self.assertEqual(len(deck), 104)

    def test_create_103_cards(self):
        deck = Deck(103)
        self.assertEqual(len(deck), 104)

    def test_create_104_cards(self):
        deck = Deck(104)
        self.assertEqual(len(deck), 104)

    def test_create_105_cards(self):
        deck = Deck(105)
        self.assertEqual(len(deck), 156)

    def test_create_200_cards(self):
        deck = Deck(200)
        self.assertEqual(len(deck), 208)

    def test_pop_none_from_empty_deck_returns_empty_list(self):
        deck = Deck(0)
        result = deck.pop_card(0)
        self.assertEqual([], result)

    def test_pop_one_from_empty_deck_returns_empty_list(self):
        deck = Deck(0)
        result = deck.pop_card()
        self.assertEqual([], result)

    def test_pop_five_from_empty_deck_returns_empty_list(self):
        deck = Deck(0)
        result = deck.pop_card(5)
        self.assertEqual([], result)

    def test_pop_two_from_deck_of_one_returns_one(self):
        deck = Deck(0)
        deck.cards.extend([self.nine])
        result = deck.pop_card(2)
        self.assertEqual([self.nine], result)
        self.assertEqual(len(deck.cards), 0)

    def test_pop_four_from_deck_of_two_returns_two(self):
        deck = Deck(0)
        deck.cards.extend([self.two, self.ace])
        result = deck.pop_card(4)
        result_contains_cards = self.two in result and self.ace in result
        self.assertTrue(result_contains_cards)
        self.assertEqual(len(deck.cards), 0)
        self.assertEqual(len(result), 2)

    def test_pop_one_from_deck_returns_one(self):
        result = self.deck.pop_card(1)
        self.assertEqual([Card(14,4)], result)

    def test_pop_one_from_deck_leaves_51(self):
        result = self.deck.pop_card(1)
        self.assertEqual([Card(14,4)], result)

    def test_pop_one_from_deck(self):
        card = self.deck.pop_card()[0]
        remaining_length = len(self.deck)
        still_in_deck = False
        for i in range(51):
            test_card = self.deck.pop_card()[0]
            if test_card == card:
                still_in_deck = True
                break
        self.assertEqual(remaining_length, 51)
        self.assertFalse(still_in_deck)

    def test_pop_three_from_deck(self):
        cards = self.deck.pop_card(3)
        remaining_length = len(self.deck)
        still_in_deck = False
        for i in range(49):
            test_card = self.deck.pop_card()[0]
            if test_card in cards:
                still_in_deck = True
                break
        self.assertEqual(remaining_length, 49)
        self.assertFalse(still_in_deck)



