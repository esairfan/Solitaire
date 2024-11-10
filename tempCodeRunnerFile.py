import pygame
import sys
from deck import Deck
from tableau import Tableau
from foundation import Foundation
from stockandwaste import StockAndWaste
from gamecontrol import PauseMenu
from missions import Missions
import time

pygame.init()
 
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Solitaire Game')

background_image = pygame.image.load('assets/background.jpg')
background_image=pygame.transform.scale(background_image, (width, height))

pygame.mixer.music.load("assets/backgroundmusic.mp3")  
pygame.mixer.music.set_volume(0.01) 
pygame.mixer.music.play(-1)   

deck = Deck()
tableau = Tableau(deck)
foundations = [Foundation(suit) for suit in ['hearts', 'diamonds', 'clubs', 'spades']]
stock_and_waste = StockAndWaste(deck)
missions = Missions(screen)

start_time = time.time()
score = 0
moves = 0  
events = []
selected_cards = []
selected_column = None
selected_foundation = None 
offset_x, offset_y = 0, 0
original_positions = []
pause_menu = PauseMenu()
foundation_positions = [(500 + i * 100, 50) for i in range(4)]
is_paused = False
pause_start_time = 0

def draw_foundations():
    for idx, foundation in enumerate(foundations):
        x, y = foundation_positions[idx]
        if foundation.cards: 
            screen.blit(foundation.cards[-1].image, (x, y))
        else: 
            pygame.draw.rect(screen, (192, 192, 192), (x, y, 80, 120), 2)
            font = pygame.font.SysFont('Arial', 15)
            suit_name = foundation.suit.capitalize()
            text = font.render(suit_name, True, (255, 255, 255))  
                         
            text_rect = text.get_rect(center=(x + 40, y + 60))
            screen.blit(text, text_rect)

def handle_mouse_button_down(event):
    global selected_cards, selected_column, selected_foundation, offset_x, offset_y, original_positions
    mouse_x, mouse_y = event.pos
 
    for idx, foundation in enumerate(foundations):
        x, y = foundation_positions[idx]
        if foundation.cards and x <= mouse_x <= x + 80 and y <= mouse_y <= y + 120:
            selected_cards = [(foundation.cards[-1], (x, y))]
            selected_foundation = idx
            offset_x, offset_y = x - mouse_x, y - mouse_y
            return
 
    if stock_and_waste.stock_position[0] <= mouse_x <= stock_and_waste.stock_position[0] + 80 and \
       stock_and_waste.stock_position[1] <= mouse_y <= stock_and_waste.stock_position[1] + 120:
        stock_and_waste.handle_click()
        pygame.display.flip()
        return
 
    if stock_and_waste.waste_pile and \
       stock_and_waste.waste_position[0] <= mouse_x <= stock_and_waste.waste_position[0] + 80 and \
       stock_and_waste.waste_position[1] <= mouse_y <= stock_and_waste.waste_position[1] + 120:
        selected_cards = [(stock_and_waste.waste_pile.pop(), stock_and_waste.waste_position)]
        offset_x, offset_y = stock_and_waste.waste_position[0] - mouse_x, stock_and_waste.waste_position[1] - mouse_y
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
                    
    if missions.is_missions_button_clicked(mouse_x, mouse_y):
        missions.display_mission_window()
        
def handle_mouse_button_up(event):
    global selected_cards, selected_column, selected_foundation, score ,moves
    if not selected_cards:
        return

    mouse_x, mouse_y = event.pos
    moving_from_waste = selected_cards[0][1] == stock_and_waste.waste_position
    valid_move_made = False
 
    for idx, foundation in enumerate(foundations):
        foundation_x, foundation_y = foundation_positions[idx]
        if foundation_x <= mouse_x <= foundation_x + 80 and foundation_y <= mouse_y <= foundation_y + 120:
            if len(selected_cards) == 1 and foundation.add_card(selected_cards[0][0]):
                valid_move_made = True
                score += 7
                moves+=1  
                 
                if selected_column is not None:
                    column = tableau.get_column(selected_column)
                    if column:
                        top_card = column[-1][0]
                        if not top_card.revealed:
                            top_card.revealed = True
                break
 
    if not valid_move_made:
        closest_column_idx = min(range(7), key=lambda i: abs(tableau.column_positions[i][0] - mouse_x))
        target_column = tableau.get_column(closest_column_idx)
        if tableau.is_valid_move(selected_cards[0][0], target_column):
            valid_move_made = True
            score += 3
            moves+=1
            
            new_x, new_y = tableau.column_positions[closest_column_idx][0], tableau.column_positions[closest_column_idx][1] + len(target_column) * 30
            for j, (card, _) in enumerate(selected_cards):
                card.revealed = True
                tableau.get_column(closest_column_idx).append((card, (new_x, new_y)))
                new_y += 30 if j == 0 else 20

            if selected_foundation is not None:
                foundations[selected_foundation].cards.pop()
            elif selected_column is not None and tableau.get_column(selected_column):
                tableau.get_column(selected_column)[-1][0].revealed = True
 
    if not valid_move_made:
        if moving_from_waste:
            stock_and_waste.waste_pile.append(selected_cards[0][0])
        elif selected_column is not None:
            for card, original_pos in zip(selected_cards, original_positions):
                tableau.get_column(selected_column).append((card[0], original_pos))
            if tableau.get_column(selected_column):
                tableau.get_column(selected_column)[-1][0].revealed = True

    selected_cards, selected_column, selected_foundation = [], None, None
    pygame.display.flip()
 
def handle_mouse_motion(event):
    if selected_cards:
        mouse_x, mouse_y = event.pos
        draw_game()

        for i, (card, _) in enumerate(selected_cards):
            y_offset = offset_y + (i * 20) if i > 0 else offset_y
            screen.blit(card.image, (mouse_x + offset_x, mouse_y + y_offset))

        pygame.display.flip()
        
def check_win_condition(): 
    return all(len(foundation.cards) == 13 for foundation in foundations)

def display_win_message(): 
    
    font = pygame.font.SysFont('Forte', 60)
    win_text = font.render("You Won the Game!", True, (255, 215, 0))  
    win_text_rect = win_text.get_rect(center=(width // 2, height // 2))
    screen.blit(win_text, win_text_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     
     
def draw_timer_and_score():
    current_time = time.time() - start_time
    minutes = int(current_time // 60)
    seconds = int(current_time % 60)
    time_text = f"Time: {minutes:02}:{seconds:02}"
    score_text = f"Score: {score}"
    move_text = f"Moves: {moves}"
    
    font = pygame.font.SysFont('Forte', 24)
    time_surface = font.render(time_text, True, (255, 255, 255))
    score_surface = font.render(score_text, True, (255, 255, 255))
    move_surface = font.render(move_text, True, (255, 255, 255))

    screen.blit(time_surface, (1000, 700))
    screen.blit(score_surface, (1000, 50))
    screen.blit(move_surface, (1000, 80))
 
def draw_game():
    screen.blit(background_image, (0, 0))
    tableau.render(screen) 
    draw_foundations()
    stock_and_waste.draw(screen)
    draw_timer_and_score()
    missions.display_missions_button()

running = True
while running: 
    events = pygame.event.get() 
    if pause_menu.is_paused:
        pause_menu.handle_events(screen,events)
    else:
        draw_game()
        
        
        if check_win_condition():
            display_win_message()
            pygame.quit()
            sys.exit()
            
       
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                handle_mouse_motion(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu.is_paused = not pause_menu.is_paused
                is_paused = pause_menu.is_paused
                if is_paused: 
                    pause_start_time = time.time()
                else: 
                    start_time += time.time() - pause_start_time
        missions.check_and_remove_completed_missions(score ,3,4,9,2,4,6,1)
    pause_menu.draw(screen)
    pygame.display.flip()

pygame.quit()
sys.exit()
