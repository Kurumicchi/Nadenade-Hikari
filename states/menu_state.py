import cv2
import pygame

class menu_state:
    def __init__(self, camera, lower_hsv, upper_hsv):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        self.side_panel = pygame.Rect(840, 0, 440, 720)
        self.content_left = 100

        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(self.content_left, 280, 280, 70)
        self.quit_button = pygame.Rect(self.content_left, 380, 280, 70)

        self.camera_rect = pygame.Rect(900, 420, 320, 240)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((245, 245, 245))
        pygame.draw.rect(
            screen,
            (235, 235, 235),
            self.side_panel
        )

        title = self.title_font.render(
            "NADENADE HIKARI",
            True,
            (40, 40, 40)
        )

        title_rect = title.get_rect(midleft=(self.content_left, 120))
        screen.blit(title, title_rect)

        self.draw_button(screen, self.start_button, "START")
        self.draw_button(screen, self.quit_button, "QUIT")

        self.draw_camera(screen)

    def draw_button(self, screen, rect, text):
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            rect,
            border_radius=12
        )

        label = self.button_font.render(
            text,
            True,
            (40, 40, 40)
        )

        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def draw_camera(self, screen):
        success, frame = self.camera.read()

        if not success:
            return

        frame = cv2.flip(frame, 1)

        # hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            hsv,
            self.lower_hsv,
            self.upper_hsv
        )

        # rgb
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, self.camera_rect.size)

        camera_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))

        screen.blit(camera_surface, self.camera_rect)
        pygame.draw.rect(
            screen,
            (40, 40, 40),
            self.camera_rect,
            width=3
        )
