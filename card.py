import pygame

class Card:
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    colors = {
        'hearts': 'red',
        'diamonds': 'red',
        'clubs': 'black',
        'spades': 'black'
    }
    image_size = (80, 120)
     
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.color = self.colors[suit]
        self.image = self.load_image()
        self.revealed = False
        
    def reveal(self):
        self.revealed = True
        
    def load_image(self):
        image_path = f'assets/{self.rank}_of_{self.suit}.png'
        original_image = pygame.image.load(image_path)
        resized_image = pygame.transform.scale(original_image, self.image_size)
        return resized_image
    
    def __repr__(self):
        return f"{self.rank} of {self.suit}"
