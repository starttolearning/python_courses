import pygame

class GameInfo:
    def __init__(self, ai_game, msg) -> None:
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        
        # Game instruction
        self.image = pygame.image.load('images/alien_invasion_start_scence.png')

        # Set the dimensions and properties of the button.
        self.width, self.height = 360, 112
        self.button_color = (151, 195, 231)
        self.text_color = (32, 58, 102)
        self.font = pygame.font.SysFont(None, 80)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(653, 368, self.width, self.height)
        self._prep_msg(msg)
    


    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def blitme(self):
        self.screen.blit(self.image, (0,0))
        self.draw_button()