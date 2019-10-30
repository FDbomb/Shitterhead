from game import Game
from card import Card

import unittest

class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game(2,3,["James", "Mark"])    
        self.two = Card(2, 1)
        self.three1 = Card(3, 1)
        self.three2 = Card(3, 2)
        self.three3 = Card(3, 3)
        self.three4 = Card(3, 4)
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
    
    def test_deal(self):
        self.game.deal()
        hands_dealt = reduce(lambda acc, p : len(p.hand) == 3 and acc,
                             self.game.players, True)
        ups_dealt = reduce(lambda acc, p : len(p.faceup) == 3 and acc,
                           self.game.players, True)
        downs_dealt = reduce(lambda acc, p : len(p.facedown) == 3 and acc,
                             self.game.players, True)
        removed_from_deck = len(self.game.deck) == 52 - 18
        self.assertTrue(hands_dealt)
        self.assertTrue(ups_dealt)
        self.assertTrue(downs_dealt)
        self.assertTrue(removed_from_deck)

    def test_first_move_one_card(self):
        self.game.players[0].hand = [self.two, self.eight, self.ace]
        self.game.players[1].hand = [self.five, self.nine, self.ten]
        self.game.first_move()
        card_dealt_from_deck = len(self.game.deck) == 51
        card_dealt_to_player = len(self.game.players[1].hand) == 3
        correct_card_laid = self.game.pile.pop() == self.five
        card_no_longer_in_hand = self.five not in self.game.players[1].hand
        moved_to_next = self.game.turn == 0
        self.assertTrue(card_dealt_from_deck)
        self.assertTrue(card_no_longer_in_hand)
        self.assertTrue(card_dealt_to_player)
        self.assertTrue(correct_card_laid)
        self.assertTrue(moved_to_next)
        
    def test_first_move_three_cards(self):
        self.game.num_cards = 4
        self.game.players[0].hand = [self.three1,
                                     self.three2,
                                     self.three3,
                                     self.two]
        self.game.players[1].hand = [self.five, self.nine, self.ten, self.eight]
        self.game.first_move()
        card_dealt_from_deck = len(self.game.deck) == 49
        card_dealt_to_player = len(self.game.players[0].hand) == 4
        cards_laid = []
        cards_laid.append(self.game.pile.pop())
        cards_laid.append(self.game.pile.pop())
        cards_laid.append(self.game.pile.pop())
        correct_cards_laid = self.three1 in cards_laid and \
                             self.three2 in cards_laid and \
                             self.three3 in cards_laid
        cards_no_longer_in_hand = self.three1 not in self.game.players[0].hand and \
                                  self.three2 not in self.game.players[0].hand and \
                                  self.three3 not in self.game.players[0].hand
        moved_to_next = self.game.turn == 1
        self.assertTrue(card_dealt_from_deck)
        self.assertTrue(card_dealt_to_player)
        self.assertTrue(correct_cards_laid)
        self.assertTrue(moved_to_next)

    def test_lay_one_card(self):
        self.game.num_cards = 4
        self.game.players[0].hand = [self.five, self.nine, self.ten, self.eight]
        self.game.lay_cards([self.nine])
        card_dealt_from_deck = len(self.game.deck) == 51
        card_dealt_to_player = len(self.game.players[0].hand) == 4
        correct_card_laid = self.game.pile.pop() == self.nine
        card_no_longer_in_hand = self.nine not in self.game.players[0].hand
        self.assertTrue(card_dealt_from_deck)
        self.assertTrue(card_dealt_to_player)
        self.assertTrue(correct_card_laid)
        self.assertTrue(card_no_longer_in_hand)
        
        
    def test_lay_three_cards(self):
        self.game.num_cards = 4
        self.game.players[1].hand = [self.five, self.three2, self.three1, self.three3]
        self.game.turn = 1
        self.game.lay_cards([self.three1, self.three3, self.three2])
        card_dealt_from_deck = len(self.game.deck) == 49
        card_dealt_to_player = len(self.game.players[1].hand) == 4
        cards_laid = []
        cards_laid.append(self.game.pile.pop())
        cards_laid.append(self.game.pile.pop())
        cards_laid.append(self.game.pile.pop())
        correct_cards_laid = self.three1 in cards_laid and \
                             self.three2 in cards_laid and \
                             self.three3 in cards_laid
        cards_no_longer_in_hand = self.three1 not in self.game.players[1].hand and \
                                  self.three2 not in self.game.players[1].hand and \
                                  self.three3 not in self.game.players[1].hand
        self.assertTrue(card_dealt_from_deck)
        self.assertTrue(card_dealt_to_player)
        self.assertTrue(correct_cards_laid)
        self.assertTrue(cards_no_longer_in_hand)
        
    def test_lay_card_inludes_deal_when_less_than_hand_size(self):
        self.game.players[0].hand = [self.five, self.three2, self.ace]
        self.game.turn = 0
        self.game.deck.cards = [self.king, self.queen]
        self.game.lay_cards([self.five])
        correct_cards_in_hand = self.queen in self.game.players[0].hand and \
                                self.three2 in self.game.players[0].hand and \
                                self.ace in self.game.players[0].hand
        correct_card_laid = self.game.pile == [self.five]
        correct_left_on_deck = self.game.deck.cards == [self.king]
        self.assertTrue(correct_cards_in_hand)
        self.assertEqual(len(self.game.players[0].hand), 3)
        self.assertEqual(self.game.pile, [self.five])
        self.assertEqual(self.game.deck.cards, [self.king])

    def test_no_deal_when_cards_laid_and_hand_big_enough(self):
        self.game.players[0].hand = [self.five, self.three2, self.ace, self.four]
        self.game.turn = 0
        self.game.deck.cards = [self.king, self.queen]
        self.game.lay_cards([self.five])
        correct_cards_in_hand = self.four in self.game.players[0].hand and \
                                self.three2 in self.game.players[0].hand and \
                                self.ace in self.game.players[0].hand
        self.assertTrue(correct_cards_in_hand)
        self.assertEqual(len(self.game.players[0].hand), 3)
        self.assertEqual(self.game.pile, [self.five])
        self.assertEqual(self.game.deck.cards, [self.king, self.queen])
        
    def test_no_deal_when_cards_laid_and_hand_big_enough(self):
        self.game.players[0].hand = [self.five, self.three2, self.ace, self.four]
        self.game.turn = 0
        self.game.deck.cards = [self.king, self.queen]
        self.game.lay_cards([self.five])
        correct_cards_in_hand = self.four in self.game.players[0].hand and \
                                self.three2 in self.game.players[0].hand and \
                                self.ace in self.game.players[0].hand
        self.assertTrue(correct_cards_in_hand)
        self.assertEqual(len(self.game.players[0].hand), 3)
        self.assertEqual(self.game.pile, [self.five])
        self.assertEqual(self.game.deck.cards, [self.king, self.queen])

    def test_deal_correct_amount_to_make_correct_hand_size(self):
        self.game.players[0].hand = [self.five]
        self.game.turn = 0
        self.game.deck.cards = [self.king, self.queen, self.ace, self.three1, self.nine]
        self.game.lay_cards([self.five])
        correct_cards_in_hand = self.nine in self.game.players[0].hand and \
                                self.three1 in self.game.players[0].hand and \
                                self.ace in self.game.players[0].hand
        self.assertTrue(correct_cards_in_hand)
        self.assertEqual(len(self.game.players[0].hand), 3)
        self.assertEqual(self.game.pile, [self.five])
        self.assertEqual(self.game.deck.cards, [self.king, self.queen])


    def test_first_current_player(self):
        player = self.game.current_player()
        self.assertEquals(player.name, "James")
                        
    def test_second_current_player(self):
        self.game.turn = 1
        player = self.game.current_player()
        self.assertEquals(player.name, "Mark")

    def test_can_lay_three_on_empty(self):
        self.assertTrue(self.game.valid_move([self.three1]))
        
    def test_can_lay_threes_on_empty(self):
        self.assertTrue(self.game.valid_move([self.three1, self.three2, self.three3]))
        
    def test_cannot_lay_different_cards(self):
        self.assertFalse(self.game.valid_move([self.ace, self.ten]))
        
    def test_can_lay_same_rank(self):
        self.game.pile.append(self.three1)
        self.assertTrue(self.game.valid_move([self.three2]))
        
    def test_can_lay_five_on_four(self):
        self.game.pile.append(self.four)
        self.assertTrue(self.game.valid_move([self.five]))

    def test_can_lay_two_on_three(self):
        self.game.pile.append(self.three1)
        self.assertTrue(self.game.valid_move([self.two]))

    def test_can_lay_seven_on_nine(self):
        self.game.pile.append(self.nine)
        self.assertTrue(self.game.valid_move([self.seven]))

    def test_can_lay_ten_on_queen(self):
        self.game.pile.append(self.queen)
        self.assertTrue(self.game.valid_move([self.ten]))

    def test_can_lay_seven_invisible(self):
        self.game.pile.extend([self.three1, self.seven])
        self.assertTrue(self.game.valid_move([self.four]))

    def test_can_play_when_playable_cards_in_hand(self):
        self.game.pile.extend([self.three1, self.ace])
        self.game.players[0].hand = [self.seven]
        self.game.players[0].faceup = [self.four]
        self.assertTrue(self.game.can_play())
        
    def test_cannot_play_when_nonplayable_cards_in_hand(self):
        self.game.pile.extend([self.three1, self.ace])
        self.game.players[0].hand = [self.king]
        self.game.players[0].faceup = [self.four]
        self.assertFalse(self.game.can_play())
        
    def test_can_play_when_playable_cards_in_faceup(self):
        self.game.pile.extend([self.three1, self.ace])
        self.game.players[0].hand = []
        self.game.players[0].faceup = [self.nine, self.ace]
        self.assertTrue(self.game.can_play())
        
    def test_cannot_play_when_nonplayable_cards_in_faceup(self):
        self.game.pile.extend([self.three1, self.ace])
        self.game.players[0].hand = []
        self.game.players[0].faceup = [self.four, self.king]
        self.assertFalse(self.game.can_play())
        
    def test_move_to_next_player(self):
        self.game.next_turn()
        self.assertEquals(self.game.turn, 1)
        
    def test_move_to_next_player_rolls(self):
        self.game.next_turn()
        self.game.next_turn()
        self.assertEquals(self.game.turn, 0)
        
    def test_lowest_player_normal_cards(self):
        self.game.players[0].hand = [self.four, self.five]
        self.game.players[1].hand = [self.three1]
        player = self.game.lowest_player()
        self.assertEquals(player.name, "Mark")
        
    def test_lowest_player_when_one_player_has_special_cards(self):
        self.game.players[0].hand = [self.seven, self.ten]
        self.game.players[1].hand = [self.three1]
        player = self.game.lowest_player()
        self.assertEquals(player.name, "Mark")        
        
    def test_lowest_player_when_one_player_has_only_special_cards(self):
        self.game.players[0].hand = [self.seven, self.ten]
        self.game.players[1].hand = [self.nine]
        player = self.game.lowest_player()
        self.assertEquals(player.name, "Mark")
        
    def test_get_cards(self):
        self.game.players[0].hand = [self.nine, self.ten, self.three1]
        self.assertEquals([self.nine, self.three1], self.game.get_cards([0,2]))

    def test_get_cards_from_faceup(self):
        self.game.players[0].hand = []
        self.game.players[0].faceup = [self.nine, self.ten, self.three1]
        self.assertEquals([self.nine, self.three1], self.game.get_cards([0,2]))

    def test_get_cards_from_facedown(self):
        self.game.players[0].hand = []
        self.game.players[0].faceup = []
        self.game.players[0].facedown = [self.nine, self.ten, self.three1]
        self.assertEquals([self.ten], self.game.get_cards([1]))

    def test_get_cards_correct_player(self):
        self.game.players[0].hand = [self.nine, self.ten, self.three1]
        self.game.players[1].hand = [self.ace, self.king, self.nine]
        self.game.turn = 1
        self.assertEquals([self.king, self.nine], self.game.get_cards([1,2]))
        
    def test_lowest_cards(self):
        self.game.players[0].hand = [self.ace, self.three1, self.nine]
        result = self.game.lowest_cards()
        self.assertEquals([self.three1], result)

    def test_lowest_cards_when_multiple_same(self):
        self.game.players[0].hand = [self.three2, self.three1, self.nine]
        result = self.game.lowest_cards()
        self.assertEquals([self.three2, self.three1], result)

    def test_pickup(self):
        self.game.pile = [self.ace, self.three1, self.nine]
        self.game.pickup()
        cards_picked_up = self.ace in self.game.players[0].hand and \
                          self.three1 in self.game.players[0].hand and \
                          self.nine in self.game.players[0].hand
        self.assertTrue(cards_picked_up)
        self.assertEquals(self.game.pile, [])
        self.assertEquals(self.game.last_move, "James picked up 3 cards.")
        self.assertEquals(self.game.turn, 1)
        
    def test_pickup_with_facedown_card(self):
        self.game.players[0].hand = []
        self.game.players[0].facedown = [self.seven, self.four, self.eight]
        self.game.pile = [self.ace, self.king, self.queen]
        self.game.pickup_with_facedown_card([self.four])
        cards_picked_up = self.ace in self.game.players[0].hand and \
                          self.king in self.game.players[0].hand and \
                          self.queen in self.game.players[0].hand and \
                          self.four in self.game.players[0].hand
        self.assertTrue(cards_picked_up)
        self.assertEquals(self.game.pile, [])
        self.assertEquals(self.game.last_move, "James picked up 4 cards.")
        self.assertEquals(self.game.turn, 1)


    def test_same_rank_returns_true(self):
        self.assertTrue(Game.same_rank([self.three1, self.three2, self.three3]))
        
    def test_same_rank_returns_true_one_card(self):
        self.assertTrue(Game.same_rank([self.nine]))

    def test_same_rank_returns_false(self):
        self.assertFalse(Game.same_rank([self.nine, self.ten]))
        
    def test_same_rank_return_false_when_two_of_three_same(self):
        self.assertFalse(Game.same_rank([self.three1, self.three1, self.ten]))
        
    def test_laid_burn_card_returns_false(self):
        self.game.pile = [self.three1, self.ten, self.ace]
        self.assertFalse(self.game.laid_burn_card())
        
    def test_laid_burn_card_returns_true(self):
        self.game.pile = [self.three1, self.ace, self.ten]
        self.assertTrue(self.game.laid_burn_card())
        
    def test_burn_when_burn_card_laid(self):
        self.game.players[0].hand = [self.five, self.nine, self.ten, self.eight]
        self.game.pile = [self.four, self.ace]
        self.game.lay_cards([self.ten])
        correct_cards_burnt = self.four in self.game.burnt and \
                              self.ace in self.game.burnt and \
                              self.ten in self.game.burnt
        self.assertEquals(self.game.pile, [])
        self.assertTrue(correct_cards_burnt)
        self.assertEquals(len(self.game.burnt), 3)
        self.assertEquals(self.game.turn, 0)
        
    def test_burn_when_four_of_a_kind_on_pile(self):
        self.game.players[0].hand = [self.five, self.nine, self.three1, self.eight]
        self.game.pile = [self.ace, self.two, self.three4, self.three2, self.three3]
        self.game.lay_cards([self.three1])
        correct_cards_burnt = self.ace in self.game.burnt and \
                              self.two in self.game.burnt and \
                              self.three4 in self.game.burnt and \
                              self.three2 in self.game.burnt and \
                              self.three3 in self.game.burnt and \
                              self.three1 in self.game.burnt
        self.assertEquals(self.game.pile, [])
        self.assertTrue(correct_cards_burnt)
        self.assertEquals(len(self.game.burnt), 6)
        self.assertEquals(self.game.turn, 0)

    def test_miss_a_go(self):
        self.game.turn = 1
        self.game.players[1].hand = [self.five, self.nine, self.three1, self.eight]
        self.game.pile = [self.ace, self.two, self.three4, self.three2, self.three3]
        self.game.lay_cards([self.eight])
        self.assertEquals(self.game.turn, 1)

    def test_miss_a_go_rolls(self):
        self.game.turn = 0
        self.game.players[0].hand = [self.five, self.nine, self.three1, self.eight]
        self.game.pile = [self.ace, self.two, self.three4, self.three2, self.three3]
        self.game.lay_cards([self.eight])
        self.assertEqual(self.game.turn, 0)
        
    def test_lay_from_face_up(self):
        self.game.turn = 0
        self.game.players[0].hand = []
        self.game.players[0].faceup = [self.three1, self.ace, self.ten]
        self.game.lay_cards([self.ace])
        self.assertEqual(self.game.players[0].faceup, [self.three1, self.ten])
        self.assertEqual(self.game.pile, [self.ace])
        
    def test_lay_from_face_down(self):
        self.game.turn = 0
        self.game.players[0].hand = []
        self.game.players[0].faveup = []
        self.game.players[0].facedown = [self.three1, self.ace, self.ten]
        self.game.lay_cards([self.ace])
        self.assertEqual(self.game.players[0].facedown, [self.three1, self.ten])
        self.assertEqual(self.game.pile, [self.ace])

    def test_playing_from_face_down(self):
        self.game.turn = 0
        self.game.players[0].hand = []
        self.game.players[0].faceup = []
        self.game.players[0].facedown = [self.three1, self.ace, self.ten]
        self.assertTrue(self.game.playing_from_face_down())
    
    def test_not_playing_from_face_down_when_hand(self):
        self.game.turn = 0
        self.game.players[0].hand = [self.ace]
        self.game.players[0].faceup = []
        self.game.players[0].facedown = [self.three1, self.ace, self.ten]
        self.assertFalse(self.game.playing_from_face_down())

    def test_not_playing_from_face_down_when_faceup(self):
        self.game.turn = 0
        self.game.players[0].hand = []
        self.game.players[0].faceup = [self.ace]
        self.game.players[0].facedown = [self.three1, self.ace, self.ten]
        self.assertFalse(self.game.playing_from_face_down())
        
    def test_continue_game_three_players(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[0].hand = [self.nine, self.ten]
        new_game.players[1].faceup = [self.ace, self.seven]
        new_game.players[2].facedown = [self.four, self.five]
        self.assertTrue(new_game.continue_game())        

    def test_continue_game_two_players(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[0].hand = [self.nine, self.ten]
        new_game.players[1].faceup = [self.ace, self.seven]
        self.assertTrue(new_game.continue_game())        

    def test_not_continue_game_one_player(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[0].hand = [self.nine, self.ten]
        self.assertFalse(new_game.continue_game())
        
    def test_get_pythonhead_when_first(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[0].hand = [self.nine, self.ten]
        pythonhead = new_game.get_pythonhead()
        self.assertEqual(pythonhead, new_game.players[0])        
        
    def test_get_pythonhead_when_second(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[1].hand = [self.nine, self.ten]
        pythonhead = new_game.get_pythonhead()
        self.assertEqual(pythonhead, new_game.players[1])        

    def test_get_pythonhead_when_third(self):
        new_game = Game(4,3,["James", "Mark", "Keith", "Steve"])
        new_game.players[2].hand = [self.nine, self.ten]
        pythonhead = new_game.get_pythonhead()
        self.assertEqual(pythonhead, new_game.players[2])        
