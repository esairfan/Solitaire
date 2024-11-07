import pygame

class Tableau:
    def __init__(self, deck):
        self.deck = deck
        self.column_positions = [(50 + i * 100, 150) for i in range(7)]
        self.cards_in_columns = [[] for _ in range(7)]
        self.setup_tableau()

    def setup_tableau(self):
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal()
                if card:
                    card.revealed = (j == i) 
                    x, y = self.column_positions[i]
                    position = (x, y + j * 30)
                    self.cards_in_columns[i].append((card, position))  

    def is_valid_move(self, card_to_move, target_column):
        if not target_column:
            return card_to_move.rank == 'K'

        top_card, _ = target_column[-1]
        opposite_color = card_to_move.color != top_card.color
        rank_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        card_to_move_index = rank_order.index(card_to_move.rank)
        top_card_index = rank_order.index(top_card.rank)
        correct_rank = (card_to_move_index + 1 == top_card_index)

        return opposite_color and correct_rank

    def render(self, screen):
        for col in self.cards_in_columns:
            for card, pos in col:
                if card.revealed:
                    screen.blit(card.image, pos)
                else:
                    card_back_image = pygame.image.load('assets/playing-card-back.jpg')
                    image_size = (80, 120)
                    card_back = pygame.transform.scale(card_back_image, image_size)
                    screen.blit(card_back, pos)

    def get_column(self, idx):
        return self.cards_in_columns[idx]

    def set_column(self, idx, cards):
        self.cards_in_columns[idx] = cards