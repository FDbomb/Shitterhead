from player import Player
from card import Card
import unittest

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.james = Player("James")
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

    def test_player_not_has_hand(self):
        self.assertFalse(self.james.has_hand())

    def test_player_has_hand_one_card(self):
        self.james.hand = [self.two]
        self.assertTrue(self.james.has_hand())

    def test_player_has_hand_two_cards(self):
        self.james.hand = [self.two, self.ace]
        self.assertTrue(self.james.has_hand())

    def test_player_not_has_faceup(self):
        self.assertFalse(self.james.has_faceup())

    def test_player_has_faceup_one_card(self):
        self.james.faceup = [self.seven]
        self.assertTrue(self.james.has_faceup())

    def test_player_has_faceup_two_cards(self):
        self.james.faceup = [self.nine, self.three]
        self.assertTrue(self.james.has_faceup())

    def test_receive_none_when_has_one(self):
        self.james.hand = [self.ten]
        self.james.receive([])
        expected_result = [self.ten]
        self.assertEqual(self.james.hand, expected_result)
        
    def test_receive_one_when_has_none(self):
        self.james.receive([self.jack])
        expected_result = [self.jack]
        self.assertEqual(self.james.hand, expected_result)

    def test_receive_one_when_has_three(self):
        self.james.hand = [self.jack, self.nine, self.ace]
        self.james.receive([self.two])
        receieved = self.jack in self.james.hand and \
                    self.nine in self.james.hand and \
                    self.ace in self.james.hand and \
                    self.two in self.james.hand and \
                    len(self.james.hand) == 4
        self.assertTrue(receieved)

    def test_receive_four(self):
        self.james.hand = [self.jack]
        self.james.receive([self.two, self.three, self.seven, self.king])
        receieved = self.jack in self.james.hand and \
                    self.two in self.james.hand and \
                    self.three in self.james.hand and \
                    self.seven in self.james.hand and \
                    self.king in self.james.hand and \
                    len(self.james.hand) == 5
        self.assertTrue(receieved)

    def test_swap(self):
        self.james.hand = [self.jack, self.nine, self.ace, self.three]
        self.james.faceup = [self.eight, self.ten, self.four, self.six]
        self.james.swap(1, 2)
        correctHand = self.jack in self.james.hand and \
                      self.ace in self.james.hand and \
                      self.three in self.james.hand and \
                      self.four in self.james.hand and \
                      len(self.james.hand) == 4
        correctFaceup = self.eight in self.james.faceup and \
                        self.ten in self.james.faceup and \
                        self.nine in self.james.faceup and \
                        self.six in self.james.faceup and \
                        len(self.james.faceup) == 4
        self.assertTrue(correctHand and correctFaceup)
    
    def test_swap_first_with_first(self):
        self.james.hand = [self.jack, self.nine, self.ace, self.three]
        self.james.faceup = [self.eight, self.ten, self.four, self.six]
        self.james.swap(0, 0)
        correctHand = self.eight in self.james.hand and \
                      self.nine in self.james.hand and \
                      self.ace in self.james.hand and \
                      self.three in self.james.hand and \
                      len(self.james.hand) == 4
        correctFaceup = self.jack in self.james.faceup and \
                        self.ten in self.james.faceup and \
                        self.four in self.james.faceup and \
                        self.six in self.james.faceup and \
                        len(self.james.faceup) == 4
        self.assertTrue(correctHand)
        self.assertTrue(correctFaceup)

    def test_swap_last_with_last(self):
        self.james.hand = [self.jack, self.nine, self.ace, self.three]
        self.james.faceup = [self.eight, self.ten, self.four, self.six]
        self.james.swap(3, 3)
        correctHand = self.jack in self.james.hand and \
                      self.nine in self.james.hand and \
                      self.ace in self.james.hand and \
                      self.six in self.james.hand and \
                      len(self.james.hand) == 4
        correctFaceup = self.eight in self.james.faceup and \
                        self.ten in self.james.faceup and \
                        self.four in self.james.faceup and \
                        self.three in self.james.faceup and \
                        len(self.james.faceup) == 4
        self.assertTrue(correctHand)
        self.assertTrue(correctFaceup)
        
    def test_swap_first_with_last(self):
        self.james.hand = [self.jack, self.nine, self.ace, self.three]
        self.james.faceup = [self.eight, self.ten, self.four, self.six]
        self.james.swap(0, 3)
        correctHand = self.six in self.james.hand and \
                      self.nine in self.james.hand and \
                      self.ace in self.james.hand and \
                      self.three in self.james.hand and \
                      len(self.james.hand) == 4
        correctFaceup = self.eight in self.james.faceup and \
                        self.ten in self.james.faceup and \
                        self.four in self.james.faceup and \
                        self.jack in self.james.faceup and \
                        len(self.james.faceup) == 4
        self.assertTrue(correctHand)
        self.assertTrue(correctFaceup)
        
    def test_player_has_cards_when_all_hands(self):
        self.james.hand = [self.jack, self.nine, self.ace]
        self.james.faceup = [self.eight, self.ten, self.four]
        self.james.facedown = [self.seven, self.three, self.six]
        self.assertTrue(self.james.has_cards())        

    def test_player_not_has_cards_when_no_hands(self):
        self.james.hand = []
        self.james.faceup = []
        self.james.facedown = []
        self.assertFalse(self.james.has_cards())        

    def test_player_has_cards_when_hand_only(self):
        self.james.hand = [self.jack, self.nine, self.ace]
        self.james.faceup = []
        self.james.facedown = []
        self.assertTrue(self.james.has_cards())        

    def test_player_has_cards_when_faceup_only(self):
        self.james.hand = []
        self.james.faceup = [self.eight, self.ten, self.four]
        self.james.facedown = []
        self.assertTrue(self.james.has_cards())        

    def test_player_has_cards_when_facedown_only(self):
        self.james.hand = []
        self.james.faceup = []
        self.james.facedown = [self.seven, self.three, self.six]
        self.assertTrue(self.james.has_cards())        
