import pygame
import time

class Missions:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('forte', 30)
        self.missions_button_rect = pygame.Rect(100, 720, 150, 50)
         
        self.all_missions = [
            {"mission": "Get the score of 200.", "function": self.score_mission_1}, 
            {"mission": "Move all four aces to the foundation within the first 30 moves.", "function": self.four_ace_mission_2},
            {"mission": "Move 3 cards from the foundation (valid moves).", "function": self.removal_of_card_from_foundation_mission_3},
            {"mission": "Remove 10 cards from the stock (valid moves).", "function": self.stoke_taken_card_mission_4}, 
            {"mission": "Successfully move 4 sequences of cards to the foundation.", "function": self.sequence_card_mission_6},
            {"mission": "Empty stock and waste piles.", "function": self.empty_stock_waste_pile_mission_7},
            {"mission": "Move 3 red cards to the foundation in a sequence.", "function": self.sequence_red_card_mission_8}
        ]
        
    def display_missions_button(self):
        text = self.font.render("Missions", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.missions_button_rect.center)
        self.screen.blit(text, text_rect)

    def is_missions_button_clicked(self, mouse_x, mouse_y):
        return self.missions_button_rect.collidepoint(mouse_x, mouse_y)

    def display_mission_window(self):
        self.screen.fill((0, 0, 0))

        mission_title_text = "Your missions are:"
        y_offset = 220
         
        mission_title_surface = self.font.render(mission_title_text, True, (255, 255, 255))
        self.screen.blit(mission_title_surface, (100, y_offset))
        y_offset += 60
 
        for i, mission in enumerate(self.all_missions):
            mission_text = f"{i + 1} - {mission['mission']}"
            text_surface = self.font.render(mission_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (100, y_offset))
            y_offset += 40

        continue_text = "Press any key to continue the game."
        continue_text_surface = self.font.render(continue_text, True, (255, 255, 255))
        self.screen.blit(continue_text_surface, (100, y_offset))
        
        pygame.display.flip()
        self.wait_for_keypress()

    def wait_for_keypress(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    waiting = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
 
    def score_mission_1(self, score):
        return score >= 200
    
    def four_ace_mission_2(self, ace_count, moves_count):
        return ace_count == 4 and moves_count <= 30
    
    def removal_of_card_from_foundation_mission_3(self, foundation_count):
        return foundation_count >= 3
    
    def stoke_taken_card_mission_4(self, stoke_count):
        return stoke_count >= 10
       
    def sequence_card_mission_6(self, card_count):
        return card_count >= 4
    
    def sequence_red_card_mission_8(self, red_card_count):
        return red_card_count >= 3
    
    def empty_stock_waste_pile_mission_7(self, empty_count):
        return empty_count >= 24
    
    def check_and_remove_completed_missions(self, score, ace_count, foundation_count, stoke_count, 
                                           card_count, red_card_count, empty_count, moves_count):
     
        for mission in self.all_missions[:]:
            mission_function = mission['function']
 
            if mission_function == self.score_mission_1:
                if mission_function(score):
                    self.remove_mission(mission)
                    return 100 
 
            elif mission_function == self.four_ace_mission_2:
                if mission_function(ace_count, moves_count):
                    self.remove_mission(mission)
                    return 100
 
            elif mission_function == self.removal_of_card_from_foundation_mission_3:
                if mission_function(foundation_count): 
                    self.remove_mission(mission)
                    return 100
 
            elif mission_function == self.stoke_taken_card_mission_4:
                if mission_function(stoke_count):
                    self.remove_mission(mission)
                    return 100
 
            elif mission_function == self.sequence_card_mission_6:
                if mission_function(card_count):
                    self.remove_mission(mission)
                    return 100
 
            elif mission_function == self.empty_stock_waste_pile_mission_7:
                if mission_function(empty_count):  
                    self.remove_mission(mission)
                    return 100
 
            elif mission_function == self.sequence_red_card_mission_8:
                if mission_function(red_card_count):
                    self.remove_mission(mission)
                    return 100
        return 0
    
    def remove_mission(self, mission):
        self.all_missions.remove(mission)
