class Foundation:
    def __init__(self, suit):
        self.suit = suit
        self.cards = []  # Corrected to 'cards' instead of 'card'
        self.rank_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def add_card(self, card):
        if self.can_add_card(card):
            self.cards.append(card)
            return True
        return False

    def can_add_card(self, card):
        if not self.cards:
            return card.suit == self.suit and card.rank == 'A'
        expected_rank = self.rank_order[len(self.cards)]  # Corrected 'card' to 'cards'
        return card.suit == self.suit and card.rank == expected_rank

    def is_complete(self):
        return len(self.card) == 13
    
    def __repr__(self):
        return f"Foundation({self.suit}): {self.cards}"