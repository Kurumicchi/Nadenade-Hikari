import cv2
import pygame
import random
from states.cursor import HandCursor
from states.game_mechanics import GameMechanics

class GameState:
    def __init__(self, camera, lower_hsv, upper_hsv):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        self.cursor = HandCursor()

        self.game_area = pygame.image.load("assets/img/game_area2.png").convert_alpha()
        self.side_panel = pygame.image.load("assets/img/side_panel.png").convert_alpha()
        self.heart = pygame.image.load("assets/img/heart.png").convert_alpha()
        self.heart_empty = pygame.image.load("assets/img/heart_empty.png").convert_alpha()
        self.heart_line = pygame.image.load("assets/img/heart_line.png").convert_alpha()
        self.scoreboard = pygame.image.load("assets/img/scoreboard.png").convert_alpha()

        self.game_area_rect = self.game_area.get_rect(topleft=(440, 0))
        self.side_panel_rect = self.side_panel.get_rect(topleft=(0, 0))
        self.scoreboard_rect = self.scoreboard.get_rect(topleft=(54, 196))
        
        self.camera_rect = pygame.Rect(60, 420, 320, 240)

        self.button_hovered = None
        self.button_pressed = None
        self.next_state = None

        self.mechanics = GameMechanics(self.game_area_rect)
        self.clock = pygame.time.Clock()

        self.flash_duration = 200
        self.shake_duration = 250
        self.shake_intensity = 7

        self.flash_timer = 0
        self.shake_timer = 0

        self.previous_health = self.mechanics.health

    def handle_event(self, event):
        if self.next_state is not None:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                self.mechanics.click(self.cursor.position)

    def update(self):
        if self.next_state is not None:
            return

        delta_time = self.clock.tick(60)
        self.mechanics.update(delta_time)

        # flash
        if self.mechanics.health < self.previous_health:
            self.flash_timer = self.flash_duration
            self.shake_timer = self.shake_duration

        self.previous_health = self.mechanics.health

        self.flash_timer = max(0, self.flash_timer - delta_time)
        self.shake_timer = max(0, self.shake_timer - delta_time)

        # game over
        if self.mechanics.health <= 0:
            self.next_state = "menu"

    def draw(self, screen):
        screen.fill((247, 248, 242))

        screen.blit(self.side_panel, self.side_panel_rect)
        self.draw_hearts(screen)

        game_surface = pygame.Surface(self.game_area.get_size(), pygame.SRCALPHA)
        game_surface.blit(self.game_area, (0, 0))

        screen.blit(self.scoreboard, self.scoreboard_rect)
        self.draw_score(screen)

        self.mechanics.draw(game_surface)

        self.flash(screen, game_surface)

        frame = self.get_camera()

        if frame is not None:
            hand_position = self.get_hand_position(frame)

            if hand_position is not None:
                self.cursor.update(hand_position)

            self.draw_camera(screen, frame)

        self.cursor.draw(screen)

    def flash(self, screen, game_surface):
        shake_x = 0
        shake_y = 0

        if self.shake_timer > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)

        game_rect = self.game_area_rect.copy()
        game_rect.x += shake_x
        game_rect.y += shake_y

        screen.blit(game_surface, game_rect)

        if self.flash_timer > 0:
            progress = self.flash_timer / self.flash_duration
            alpha = int(150 * progress)

            red_overlay = pygame.Surface(game_surface.get_size(), pygame.SRCALPHA)

            red_overlay.fill((255, 0, 0, alpha))

            screen.blit(red_overlay, game_rect)

    def draw_hearts(self, screen):
        heart_x = 52
        heart_y = 66 
        heart_gap = 15

        screen.blit(self.heart_line, (42, 154))

        for i in range(3):
            x = heart_x + i * (97 + heart_gap)

            if i < self.mechanics.health:
                heart_image = self.heart
            else:
                heart_image = self.heart_empty

            screen.blit(heart_image, (x, heart_y))

    def draw_score(self, screen):
        font = pygame.font.Font("assets/font/Fredoka-Bold.ttf", 72)

        score_text = str(self.mechanics.score)

        text = font.render(score_text, True, (255, 249, 222))
        outline_color = (66, 49, 77)
        outline_width = 3

        text_area = pygame.Rect(90, 255, 238, 90)
        text_rect = text.get_rect(center=text_area.center)

        outline = font.render(score_text, True, outline_color)

        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx * dx + dy * dy <= outline_width * outline_width:
                    outline_rect = text_rect.move(dx, dy)
                    screen.blit(outline, outline_rect)

        screen.blit(text, text_rect)

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

