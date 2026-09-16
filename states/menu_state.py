import cv2
import pygame
from states.cursor import handcursor

class menu_state:
    def __init__(self, camera, lower_hsv, upper_hsv):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        self.cursor = handcursor()

        self.side_panel = pygame.Rect(0, 0, 440, 720)
        self.content_right = 500

        self.title_font = pygame.font.Font(None, 64)
        self.button_font = pygame.font.Font(None, 48)

        self.start_button = pygame.Rect(self.content_right, 280, 280, 70)
        self.quit_button = pygame.Rect(self.content_right, 380, 280, 70)
        self.button_hovered = None

        self.camera_rect = pygame.Rect(60, 420, 320, 240)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.button_hovered == "start":
                    print("start")
                elif self.button_hovered == "quit":
                    print("quit")
            
    def update(self):
        cursor_rect = pygame.Rect(
            self.cursor.position[0] - self.cursor.radius,
            self.cursor.position[1] - self.cursor.radius,
            self.cursor.radius * 2,
            self.cursor.radius * 2
        )

        if cursor_rect.colliderect(self.start_button):
            self.button_hovered = "start"
        elif cursor_rect.colliderect(self.quit_button):
            self.button_hovered = "quit"
        else:
            self.button_hovered = None


    """
    warna bagus:
    79B88A (121, 184, 138) green
    3F7350 (63, 115, 80) dark green
    B8DDBF (184, 221, 191) light green
    """

    def draw(self, screen):
        screen.fill((247, 248, 242))
        pygame.draw.rect(
            screen,
            (221, 235, 221),
            self.side_panel
        )

        title = self.title_font.render(
            "NADENADE HIKARI",
            True,
            (40, 40, 40)
        )

        title_rect = title.get_rect(midleft=(self.content_right, 120))
        screen.blit(title, title_rect)

        self.draw_button(
            screen,
            self.start_button,
            "START",
            self.button_hovered == "start"
        )
        self.draw_button(
            screen,
            self.quit_button,
            "QUIT",
            self.button_hovered == "quit"
        )

        frame = self.get_camera()

        if frame is not None:
            hand_position = self.get_hand_position(frame)

            if hand_position is not None:
                self.cursor.update(hand_position)

            self.draw_camera(screen, frame)

        self.cursor.draw(screen)

    def draw_button(self, screen, rect, text, hovered=False):
        if hovered:
            color = (200, 200, 200)
        else:
            color = (220, 220, 220)

        pygame.draw.rect(
            screen,
            color,
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





"""
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

        moments = cv2.moments(mask)

        hand_position = None

        if moments["m00"] != 0:
            hand_x = int(moments["m10"] / moments["m00"])
            hand_y = int(moments["m01"] / moments["m00"])
            frame_height, frame_width = frame.shape[:2]
            screen_x = int(hand_x / frame_width * 1280)
            screen_y = int(hand_y / frame_height * 720)
            hand_position = (screen_x, screen_y)

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

        return hand_position
"""