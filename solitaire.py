import pygame
import sys
from deck import Deck  

pygame.init()

width, height = 1200, 1000  #  Dimensions of the window

screen = pygame.display.set_mode((width, height))  # Game Play on which all animations or elements are shown
pygame.display.set_caption('Solitaire Game')

deck = Deck()  # Collection of Cards
column_positions = [(50 + i * 100, 150) for i in range(7)]  # Position where cards are placed on screen
cards_in_columns = [[] for _ in range(7)]  # List of lists for storing cards for tableau

# Deal cards into columns
for i in range(7):  
    for j in range(i + 1):  
        card = deck.deal()
        if card:
            x, y = column_positions[i] 
            position = (x, y + j * 30) 
            cards_in_columns[i].append((card, position))  

card_back_image = pygame.image.load('assets/playing-card-back.jpg')  # Image for all back cards before top elements
image_size = (80, 120)  # Size of Back Image 
card_back = pygame.transform.scale(card_back_image, image_size)  # Resizing of Back Image

selected_card = None   # Card which is to be dragged
selected_column = None # Column from where the card is dragged 
offset_x = 0  # X pos of card when dragged
offset_y = 0  # Y pos of card when dragged
original_pos = None   # Original position of card when dragged

def is_valid_move(card_to_move, target_column):
    if not target_column:
        return card_to_move.rank == 'K'
     
    top_card, _ = target_column[-1]
    opposite_color = card_to_move.color != top_card.color
    
    rank_order = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    card_to_move_index = rank_order.index(card_to_move.rank)
    top_card_index = rank_order.index(top_card.rank)
    correct_rank = (card_to_move_index + 1 == top_card_index)
    
    return opposite_color and correct_rank

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos 
            for col_idx, col in enumerate(cards_in_columns):
                if col:
                    card, pos = col[-1]
                    card_x, card_y = pos
                    if card_x <= mouse_x <= card_x + card.image.get_width() and card_y <= mouse_y <= card_y + card.image.get_height():
                        selected_card = card
                        selected_column = col_idx
                        original_pos = pos  
                        offset_x = card_x - mouse_x
                        offset_y = card_y - mouse_y
                        cards_in_columns[col_idx] = col[:-1] 
                        break
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_card:
                mouse_x, mouse_y = event.pos
                new_pos = (mouse_x + offset_x, mouse_y + offset_y)
             
                closest_column_idx = min(range(7), key=lambda i: abs(column_positions[i][0] - mouse_x))
                target_column = cards_in_columns[closest_column_idx]
                
                if is_valid_move(selected_card, target_column):
                    new_x = column_positions[closest_column_idx][0] 
                    new_y = column_positions[closest_column_idx][1] + len(target_column) * 30  
                    cards_in_columns[closest_column_idx].append((selected_card, (new_x, new_y)))
                else: 
                    cards_in_columns[selected_column].append((selected_card, original_pos)) 

                selected_card = None
                pygame.display.flip()
        
        elif event.type == pygame.MOUSEMOTION:
            if selected_card:
                mouse_x, mouse_y = event.pos 
                screen.fill((0, 128, 0))  
                
                for col in cards_in_columns:
                    for i, (card, pos) in enumerate(col):
                        if i == len(col) - 1:  
                            screen.blit(card.image, pos)
                        else:  
                            screen.blit(card_back, pos)
                             
                screen.blit(selected_card.image, (mouse_x + offset_x, mouse_y + offset_y))
                pygame.display.flip()
                continue
 
    screen.fill((0, 128, 0))  
    
    for col in cards_in_columns:
        for i, (card, pos) in enumerate(col):
            if i == len(col) - 1: 
                screen.blit(card.image, pos)
            else:
                screen.blit(card_back, pos)

    pygame.display.flip()
