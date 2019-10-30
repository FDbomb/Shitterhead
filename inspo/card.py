class Card:
        
    suits = {1: 'CLUBS', 2: 'DIAMONDS', 3:'HEARTS', 4:'SPADES'}
    ranks = {2:'TWO', 3:'THREE', 4:'FOUR', 5:'FIVE', 6:'SIX', 7:'SEVEN', 
            8:'EIGHT',9: 'NINE', 10:'TEN', 11:'JACK', 12:'QUEEN', 13:'KING',
            14:'ACE'}

    lay_on_anything_ranks = [2,7,10]
    invisible = 7
    burn = 10
    miss_a_go = 8

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
         
    def __str__(self):
        return ((Card.ranks[self.rank]) +  ' of ' + (Card.suits[self.suit]))

    def __lt__(self, other):
        return self.rank < other.rank
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

def sh_cmp(card):
    if card.rank in Card.lay_on_anything_ranks:
        return 15
    else:
        return card.rank  