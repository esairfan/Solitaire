import pygame 
import sys

class PauseMenu:
    def __init__(self):
        self.is_paused = False
        self.pause_surface = pygame.Surface((200, 100))
        self.pause_surface.fill((200, 200, 200))
        self.font = pygame.font.SysFont('Arial', 20)
        self.continue_text = self.font.render("Continue", True, (0, 0, 0))
        self.exit_text = self.font.render("Exit", True, (0, 0, 0))
        
        # Adjusting rects for text to position correctly on the pause_surface
        self.continue_rect = self.continue_text.get_rect(center=(self.pause_surface.get_width() // 2, 30))
        self.exit_rect = self.exit_text.get_rect(center=(self.pause_surface.get_width() // 2, 70))

    def handle_events(self,screen , events):
        if self.is_paused:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    # Convert mouse position relative to the pause menu surface position
                    rel_x = mouse_x - (screen.get_width() // 2 - 100)
                    rel_y = mouse_y - (screen.get_height() // 2 - 50)

                    # Check if the mouse click is within the rects
                    if self.continue_rect.collidepoint(rel_x, rel_y):
                        self.is_paused = False
                    elif self.exit_rect.collidepoint(rel_x, rel_y):
                        pygame.quit()
                        sys.exit()

    def draw(self, screen):
        if self.is_paused:
            screen.blit(self.pause_surface, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))
            self.pause_surface.blit(self.continue_text, self.continue_rect)
            self.pause_surface.blit(self.exit_text, self.exit_rect)
            screen.blit(self.pause_surface, (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))