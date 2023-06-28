import pygame


class Button:
    def __init__(self, x, y, width, height, inactive_color, active_color, text, text_font, text_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.text = text

        # Setting up the font for the text
        self.text_font = pygame.font.SysFont(text_font, text_size)

    def draw(self, screen):
        """Method that checks if button was touched with mouse and also displays button's
        frame and text on the screen"""
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.active_color, self.rect)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect)
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)  # Draw the frame with a thickness of 3 pixels

        text_surface = self.text_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Method that checks if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
