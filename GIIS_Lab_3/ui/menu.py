import pygame

class Menu:
    def __init__(self, options):
        self.options = options
        self.selected = options[0]
        self.buttons = []
        for i,opt in enumerate(options):
            rect = pygame.Rect(10, 10 + i*30, 100, 25)
            self.buttons.append((opt, rect))

    def draw(self, screen):
        font = pygame.font.SysFont(None, 24)
        for opt,rect in self.buttons:
            color = (200,200,200) if opt==self.selected else (150,150,150)
            pygame.draw.rect(screen, color, rect)
            text = font.render(opt, True, (0,0,0))
            screen.blit(text, (rect.x+5, rect.y+3))

    def handle_click(self, pos):
        for opt,rect in self.buttons:
            if rect.collidepoint(pos):
                self.selected = opt
                return True
        return False

    def get_mode(self):
        return self.selected