from deck import Deck
from player import Player
from card import Card, sh_cmp

class Game:

    def __init__(self, num_players, num_cards, player_names):
        self.num_players = num_players
        self.num_cards = num_cards
        self.players = []
        self.deck = Deck(self.num_players * self.num_cards * 3) 
        self.pile = []
        self.burnt = []
        self.turn = 0
        self.last_move = ""
        for i in range(num_players):
            player = Player(player_names[i])
            self.players.append(player)

    def deal(self):
        self.deck.shuffle()
        for i in range(self.num_players):
            for j in range(self.num_cards):
                self.players[i].hand.extend(self.deck.pop_card())
                self.players[i].faceup.extend(self.deck.pop_card())
                self.players[i].facedown.extend(self.deck.pop_card())
        for i in range(self.num_players):
            self.players[i].hand.sort(key=sh_cmp)

    def first_move(self):
        self.turn = self.players.index(self.lowest_player())
        cards = self.lowest_cards()
        self.lay_cards(cards)
            
    def lay_cards(self, cards):
        did_burn = False
        player = self.current_player()
        if player.has_hand():
            self.play_from_hand(cards)
        elif player.has_faceup():
            self.play_from_faceup(cards)
        else:
            self.play_from_facedown(cards)
        self.last_move = player.name + " laid: " +  ", ".join(map(str, cards))
        if (self.laid_burn_card() or self.four_of_a_kind_on_pile()):
            self.burn_pile()
        else:
            self.next_turn()
            if (self.laid_miss_a_go_card()):
                self.next_turn()
        
    def burn_pile(self):
        self.burnt.extend(self.pile)
        self.pile = []

    def play_from_hand(self, cards):
        self.pile.extend(cards)
        player = self.current_player()
        player.hand = Game.remove_cards(cards, player.hand)
        while len(player.hand) < self.num_cards and self.deck.cards:
            player.receive(self.deck.pop_card())
        player.hand.sort(key=sh_cmp)

    def play_from_faceup(self, cards):
        self.pile.extend(cards)
        player = self.current_player()
        player.faceup = Game.remove_cards(cards, player.faceup)

    def play_from_facedown(self, cards):
        self.pile.extend(cards)
        player = self.current_player()
        player.facedown = Game.remove_cards(cards, player.facedown)

    def laid_burn_card(self):
        return (self.pile[-1].rank == Card.burn)
    
    def four_of_a_kind_on_pile(self):
        return (len(self.pile) >= 4 and Game.same_rank(self.pile[-4:]))

    def laid_miss_a_go_card(self):
        return (self.pile[-1].rank == Card.miss_a_go)
    
    def current_player(self):
        return self.players[self.turn]
    
    def valid_move(self, cards):
        if not Game.same_rank(cards):
            return False
        else:
            return Game.can_lay(cards[0], self.pile)

    def can_play(self):
        player = self.current_player()
        if player.has_hand():
            return self.can_play_from_hand()
        elif player.has_faceup():
            return self.can_play_from_faceup()
        else:
            return player.has_facedown()
        
    def can_play_from_hand(self):
        player = self.current_player()
        return self.can_lay_any_of(player.hand)
        
    def can_play_from_faceup(self):
        player = self.current_player()
        return self.can_lay_any_of(player.faceup)

    def can_lay_any_of(self, cards):
        return any(map(lambda c : Game.can_lay(c, self.pile), cards))

    def next_turn(self):
        self.turn = self.turn + 1
        if self.turn == len(self.players):
            self.turn = 0

    def lowest_player(self):
        player_lowest = self.players[0]
        for player in self.players:
            if sh_cmp(min(player.hand, key=sh_cmp)) < sh_cmp(min(player_lowest.hand,
                                                  key=sh_cmp)):
                player_lowest = player
        return player_lowest       
    
    def get_cards(self, card_indexes):
        player = self.current_player()
        if player.has_hand():
            return self.get_from_indexes(card_indexes, player.hand)
        elif player.has_faceup():
            return self.get_from_indexes(card_indexes, player.faceup)
        else:
            return self.get_from_indexes(card_indexes, player.facedown)

    def get_from_indexes(self, indexes, cards):
        return map(lambda i : cards[i], indexes)

    def lowest_cards(self):
        player = self.current_player()
        cards = [min(player.hand, key=sh_cmp)]
        cards.extend([c for c in player.hand
                             if c.rank == cards[0].rank
                             and c != cards[0]])
        return cards

    def pickup(self):
        player = self.current_player()
        player.receive(self.pile)
        player.hand.sort(key=sh_cmp)
        self.last_move = player.name + " picked up " + str(len(self.pile)) + " cards."
        self.pile = []
        self.next_turn()
    
    def pickup_with_facedown_card(self, card):
        player = self.current_player()
        player.receive(self.pile)
        player.receive(card)
        player.facedown = Game.remove_cards(card, player.facedown)
        player.hand.sort(key=sh_cmp)
        self.last_move = player.name + " picked up " + str(len(self.pile) + 1) + " cards."
        self.pile = []
        self.next_turn()
        
    def playing_from_face_down(self):
        player = self.current_player()
        result = not player.has_hand() and not player.has_faceup() and player.has_facedown()
        return result
    
    def continue_game(self):
        players_with_cards = 0
        for player in self.players:
            if player.has_cards():
                players_with_cards = players_with_cards + 1
        return players_with_cards >= 2

    def get_pythonhead(self):
        for player in self.players:
            if player.has_cards():
                return player

    @staticmethod
    def same_rank(cards):
        return all(map(lambda c : c.rank == cards[0].rank, cards))

    @staticmethod
    def can_lay(card, pile):
        if not pile:
            return True
        elif card.rank in Card.lay_on_anything_ranks:
            return True
        else:
            card_on_pile = pile[-1]
            rest_of_pile = pile[0:-1]
            if card_on_pile.rank == Card.invisible:
                return Game.can_lay(card, rest_of_pile)
            else:
                return card.rank >= card_on_pile.rank

    @staticmethod
    def remove_cards(cards_to_remove, cards):
        return filter(lambda c : c not in cards_to_remove, cards)
