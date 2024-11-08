import pygame

class StockAndWaste:
    def __init__(self, deck):
        self.stock_pile = deck.cards[:]  
        self.waste_pile = []
        
        self.stock_position = (50, 50)
        self.waste_position = (150, 50)
        
        self.card_back_image = pygame.image.load('assets/playing-card-back.jpg')
        self.card_back_image = pygame.transform.scale(self.card_back_image, (80, 120))

    def draw(self, screen):
        if self.stock_pile:
            screen.blit(self.card_back_image, self.stock_position)
        else:
            pygame.draw.rect(screen, (200, 200, 200), (*self.stock_position, 80, 120), 2)

        if self.waste_pile:
            top_card = self.waste_pile[-1]
            screen.blit(top_card.image, self.waste_position)
        else:
            pygame.draw.rect(screen, (200, 200, 200), (*self.waste_position, 80, 120), 2)

    def handle_click(self):
        if self.stock_pile:
            self.waste_pile.append(self.stock_pile.pop(0))
        elif self.waste_pile:
            self.stock_pile = self.waste_pile[:]
            self.waste_pile.clear()
