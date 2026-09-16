import pygame

class handcursor:
    def __init__(self, radius=15):
        self.position = (0, 0)
        self.radius = radius

    def update(self, position):
        self.position = position

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            self.position,
            self.radius
        )