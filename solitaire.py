import pygame
import sys
from deck import Deck
from tableau import Tableau
from foundation import Foundation
from stockandwaste import StockAndWaste 

pygame.init()

width, height = 1200, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solitaire Game')

deck = Deck()
tableau = Tableau(deck)
foundations = [Foundation(suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades']]
stock_and_waste = StockAndWaste(deck)

selected_cards = []
selected_column = None
offset_x, offset_y = 0, 0
original_positions = []

foundation_positions = [(500 + i * 100, 50) for i in range(4)]

def draw_gradient_background(surface):
    w, h = surface.get_size()
    rect = pygame.Rect(0, 0, w, h)
    gradient = pygame.Surface(rect.size, pygame.SRCALPHA)
    y1 = rect.top
    y2 = rect.bottom

    red_range = 255 - 0
    green_range = 255 - 128
    blue_range = 224 - 0

    for y in range(y1, y2):
        ratio = (y - y1) / (y2 - y1)

        red = int(0 + (red_range * ratio))
        green = int(128 + (green_range * ratio))
        blue = int(0 + (blue_range * ratio))

        color = (red, green, blue)
        line = pygame.Surface((w, 1), pygame.SRCALPHA)
        line.fill(color)
        gradient.blit(line, (0, y))
    surface.blit(gradient, (0, 0))
    
def draw_foundations():
    for idx, foundation in enumerate(foundations):
        x, y = foundation_positions[idx]

        if foundation.cards:
            screen.blit(foundation.cards[-1].image, (x, y))
        else:
            pygame.draw.rect(screen, (200, 200, 200), (x, y, 80, 120), 2)
            font = pygame.font.SysFont('Arial', 15)
            suit_name = foundation.suit.capitalize()
            text = font.render(suit_name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + 40, y + 60))
            screen.blit(text, text_rect)

def handle_mouse_button_down(event):
    global selected_cards, selected_column, offset_x, offset_y, original_positions
    mouse_x, mouse_y = event.pos
    
    if stock_and_waste.stock_position[0] <= mouse_x <= stock_and_waste.stock_position[0] + 80 and \
       stock_and_waste.stock_position[1] <= mouse_y <= stock_and_waste.stock_position[1] + 120:
        stock_and_waste.handle_click()
        pygame.display.flip()
        return
    
    for col_idx in range(7):
        col = tableau.get_column(col_idx)
        if col and col[-1][0].revealed:
            for i, (card, pos) in enumerate(col):
                card_x, card_y = pos
                if card.revealed and card_x <= mouse_x <= card_x + card.image.get_width():
                    if (i == len(col) - 1 and card_y <= mouse_y <= card_y + card.image.get_height()) or \
                       (i < len(col) - 1 and card_y <= mouse_y <= card_y + card.image.get_height() - 90):
                        selected_column = col_idx
                        selected_cards = col[i:]
                        original_positions = [pos for _, pos in selected_cards]
                        tableau.set_column(selected_column, col[:i])
                        offset_x, offset_y = card_x - mouse_x, card_y - mouse_y
                        break

def handle_mouse_button_up(event):
    global selected_cards, selected_column
    if not selected_cards:
        return

    mouse_x, mouse_y = event.pos

    for idx, foundation in enumerate(foundations):
        foundation_x, foundation_y = foundation_positions[idx]
        if foundation_x <= mouse_x <= foundation_x + 80 and foundation_y <= mouse_y <= foundation_y + 120:
            if len(selected_cards) == 1 and foundation.add_card(selected_cards[0][0]):
                if selected_column is not None and tableau.get_column(selected_column):
                    tableau.get_column(selected_column)[-1][0].revealed = True
                selected_cards, selected_column = [], None
                pygame.display.flip()
                return

    closest_column_idx = min(range(7), key=lambda i: abs(tableau.column_positions[i][0] - mouse_x))
    target_column = tableau.get_column(closest_column_idx)

    if tableau.is_valid_move(selected_cards[0][0], target_column):
        new_x, new_y = tableau.column_positions[closest_column_idx][0], tableau.column_positions[closest_column_idx][1] + len(target_column) * 30
        for j, (card, _) in enumerate(selected_cards):
            tableau.get_column(closest_column_idx).append((card, (new_x, new_y)))
            new_y += 30 if j == 0 else 20
 
        if selected_column is not None and tableau.get_column(selected_column):
            tableau.get_column(selected_column)[-1][0].revealed = True

    else:
        for card, original_pos in zip(selected_cards, original_positions):
            tableau.get_column(selected_column).append((card[0], original_pos))
            
        if selected_column is not None and tableau.get_column(selected_column):
            tableau.get_column(selected_column)[-1][0].revealed = True

    selected_cards, selected_column = [], None
    pygame.display.flip()

def handle_mouse_motion(event):
    if selected_cards:
        mouse_x, mouse_y = event.pos
        draw_gradient_background(screen)
        tableau.render(screen)
        draw_foundations()
        stock_and_waste.draw(screen)

        for i, (card, _) in enumerate(selected_cards):
            y_offset = offset_y + (i * 20) if i > 0 else offset_y
            screen.blit(card.image, (mouse_x + offset_x, mouse_y + y_offset))

        pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_button_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_button_up(event)
        elif event.type == pygame.MOUSEMOTION:
            handle_mouse_motion(event)

    draw_gradient_background(screen)
    tableau.render(screen)
    draw_foundations()
    stock_and_waste.draw(screen)  
    pygame.display.flip()
