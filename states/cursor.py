import pygame

class HandCursor:
    def __init__(self):
        self.position = (0, 0)
        self.cursor = pygame.image.load("assets/img/cursor.png").convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (48, 48))

    def update(self, position):
        self.position = position

    def draw(self, screen):
        x, y = self.position

        screen.blit(
            self.cursor,
            (
                x - self.cursor.get_width() // 2,
                y - self.cursor.get_height() // 2
            )
        )