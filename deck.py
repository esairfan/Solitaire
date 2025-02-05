import random 
from card import Card

class Deck:
    def __init__(self):
        self.cards = [Card(suit,rank)for suit in Card.suits for rank in Card.ranks]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop() if self.cards else None