from card import Card, sh_cmp
from random import shuffle
import unittest

class TestCard(unittest.TestCase):

    def setUp(self):
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
    
    def test_normal_order(self):
        cards = [self.three, self.four, self.five, self.six, self.eight,
                 self.nine, self.jack, self.queen, self.king]
        expected_result = [self.three, self.four, self.five, self.six,
                           self.eight, self.nine, self.jack, self.queen,
                           self.king]
        shuffle(cards)
        cards.sort(key=sh_cmp)
        self.assertEqual(cards, expected_result)

    def test_two_higher_than_ace(self):
        cards = [self.two, self.ace]
        expected_result = [self.ace, self.two]
        cards.sort(key=sh_cmp)
        self.assertEqual(cards, expected_result)
        
    def test_ten_higher_than_king(self):
        cards = [self.ten, self.king]
        expected_result = [self.king, self.ten]
        cards.sort(key=sh_cmp)
        self.assertEqual(cards, expected_result)

    def test_seven_higher_than_eight(self):
        cards = [self.seven, self.eight]
        expected_result = [self.eight, self.seven]
        cards.sort(key=sh_cmp)
        self.assertEqual(cards, expected_result)
    
    def test_cards_equal(self):
        card1 = Card(3,2)
        card2 = Card(3,2)
        self.assertEqual(card1, card2)

    def test_cards_not_equal(self):
        card1 = Card(3,2)
        card2 = Card(3,1)
        self.assertNotEqual(card1, card2)
