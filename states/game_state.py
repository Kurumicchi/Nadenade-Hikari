import cv2
import pygame
import random
from states.cursor import handcursor

class game_state:
    def __init__(self, camera, lower_hsv, upper_hsv):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        self.cursor = handcursor()

        self.game_area = pygame.image.load("assets/img/game_area.png").convert_alpha()
        self.side_panel = pygame.image.load("assets/img/side_panel.png").convert_alpha()

        self.game_area_rect = self.game_area.get_rect(topleft=(440, 0))
        self.side_panel_rect = self.side_panel.get_rect(topleft=(0, 0))
        
        self.camera_rect = pygame.Rect(60, 420, 320, 240)

        self.button_hovered = None
        self.button_pressed = None
        self.next_state = None

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((247, 248, 242))

        screen.blit(self.game_area, self.game_area_rect)
        screen.blit(self.side_panel, self.side_panel_rect)

        frame = self.get_camera()

        if frame is not None:
            hand_position = self.get_hand_position(frame)

            if hand_position is not None:
                self.cursor.update(hand_position)

            self.draw_camera(screen, frame)

        self.cursor.draw(screen)

    def get_camera(self):
        success, frame = self.camera.read()

        if not success:
            return None

        return cv2.flip(frame, 1)

    def get_hand_position(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(
            hsv,
            self.lower_hsv,
            self.upper_hsv
        )

        moments = cv2.moments(mask)

        if moments["m00"] == 0:
            return None

        hand_x = int(moments["m10"] / moments["m00"])
        hand_y = int(moments["m01"] / moments["m00"])

        frame_height, frame_width = frame.shape[:2]

        screen_x = int(hand_x / frame_width * 1280)
        screen_y = int(hand_y / frame_height * 720)

        return (screen_x, screen_y)

    def draw_camera(self, screen, frame):
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

