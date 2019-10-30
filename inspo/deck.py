from random import shuffle

from card import Card

class Deck:

    def __init__(self, cards_required):
        one_deck = [Card(x,y) for y in Card.suits for x in Card.ranks]
        self.cards = []
        while len(self.cards) < cards_required:
            self.cards.extend(one_deck)

    def __len__(self):
        return len(self.cards)

    def shuffle(self):
        shuffle(self.cards)

    def pop_card(self, num=1):
        if not self.cards:
            return []
        else:
            cards = []
            if num >= len(self.cards):
                cards.extend(self.cards)
                self.cards = []
            else:
                for i in range(num):
                    cards.append(self.cards.pop())
            return cards            
