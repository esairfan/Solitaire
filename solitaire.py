import pygame
import sys
from deck import Deck
from tableau import Tableau

pygame.init()

width, height = 1200, 1000  
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solitaire Game')

deck = Deck()
tableau = Tableau(deck)  

selected_cards = []
selected_column = None
offset_x = 0
offset_y = 0
original_positions = []

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            for col_idx in range(7):
                col = tableau.get_column(col_idx)
                if col and col[-1][0].revealed:
                    for i, (card, pos) in enumerate(col):
                        if card.revealed:
                            card_x, card_y = pos
                            if card_x <= mouse_x <= card_x + card.image.get_width() and card_y <= mouse_y <= card_y + card.image.get_height():
                                selected_column = col_idx
                                selected_cards = col[i:]  
                                original_positions = [pos for _, pos in selected_cards] 
                                tableau.set_column(selected_column, col[:i])  
                                offset_x = card_x - mouse_x
                                offset_y = card_y - mouse_y
                                break

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_cards:
                mouse_x, mouse_y = event.pos
                closest_column_idx = min(range(7), key=lambda i: abs(tableau.column_positions[i][0] - mouse_x))
                target_column = tableau.get_column(closest_column_idx)

                if tableau.is_valid_move(selected_cards[0][0], target_column):
                    new_x = tableau.column_positions[closest_column_idx][0]
                    new_y = tableau.column_positions[closest_column_idx][1] + len(target_column) * 30

                    for card, _ in selected_cards:
                        tableau.get_column(closest_column_idx).append((card, (new_x, new_y)))
                        new_y += 30  # Stack cards vertically

                    if tableau.get_column(selected_column):
                        tableau.get_column(selected_column)[-1][0].revealed = True  
                else:
                    for card, original_pos in zip(selected_cards, original_positions):
                        tableau.get_column(selected_column).append((card[0], original_pos))

                    if tableau.get_column(selected_column):
                        tableau.get_column(selected_column)[-1][0].revealed = True

                selected_cards = []
                selected_column = None
                pygame.display.flip()

        elif event.type == pygame.MOUSEMOTION:
            if selected_cards:
                mouse_x, mouse_y = event.pos
                screen.fill((0, 128, 0)) 

                tableau.render(screen)  

                for i, (card, _) in enumerate(selected_cards):
                    screen.blit(card.image, (mouse_x + offset_x, mouse_y + offset_y + i * 20)) 

                pygame.display.flip() 
                continue

    screen.fill((0, 128, 0))  
    tableau.render(screen)  
    pygame.display.flip() 