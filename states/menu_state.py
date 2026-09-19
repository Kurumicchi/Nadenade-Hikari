import cv2
import pygame
import random
from states.cursor import handcursor

class menu_state:
    def __init__(self, camera, lower_hsv, upper_hsv):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv

        pygame.mixer.music.load("assets/audio/tatamusic_chiptune_video_game_games_music.mp3")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, fade_ms=1000)
        self.choo_choo = pygame.mixer.Sound("assets/audio/choo_choo.mp3")
        self.choo_choo.set_volume(0.2)
        self.next_choo_time = pygame.time.get_ticks() + random.randint(5000, 10000)

        self.cursor = handcursor()
        self.content_right = 500

        self.game_area = pygame.image.load("assets/img/game_area.png").convert_alpha()
        # self.game_area = pygame.transform.smoothscale(self.game_area, (840, 720))
        self.side_panel = pygame.image.load("assets/img/side_panel.png").convert_alpha()

        
        self.title = pygame.image.load("assets/img/title.png").convert_alpha()
        self.high_score = pygame.image.load("assets/img/high_score.png").convert_alpha()
        self.start_image = pygame.image.load("assets/img/start_idle.png").convert_alpha()
        self.start_hovered_image = pygame.image.load("assets/img/start_hovered.png").convert_alpha()
        self.start_pressed_image = pygame.image.load("assets/img/start_pressed.png").convert_alpha()
        self.quit_image = pygame.image.load("assets/img/quit_idle.png").convert_alpha()
        self.quit_hovered_image = pygame.image.load("assets/img/quit_hovered.png").convert_alpha()
        self.quit_pressed_image = pygame.image.load("assets/img/quit_pressed.png").convert_alpha()

        self.cloud_1 = pygame.image.load("assets/img/cloud_1.png").convert_alpha()
        self.cloud_2 = pygame.image.load("assets/img/cloud_2.png").convert_alpha()
        self.cloud_3 = pygame.image.load("assets/img/cloud_3.png").convert_alpha()
        self.cloud_4 = pygame.image.load("assets/img/cloud_4.png").convert_alpha()

        self.game_area_rect = self.game_area.get_rect(topleft=(440, 0))
        self.side_panel_rect = self.side_panel.get_rect(topleft=(0, 0))
        self.title_rect = self.title.get_rect(topleft=(478, 60))
        self.high_score_rect = self.high_score.get_rect(topleft=(22, 44))
        self.start_rect = self.start_image.get_rect(topleft=(498, 318))
        self.quit_rect = self.quit_image.get_rect(topleft=(852, 318))
        self.start_hitbox = pygame.Rect(self.start_rect.x + 29, self.start_rect.y + 97,  247, 99)
        self.quit_hitbox = pygame.Rect(self.quit_rect.x + 29, self.quit_rect.y + 97,  247, 99)

        self.clouds = [
            {
                "image": self.cloud_1,
                "rect": self.cloud_1.get_rect(topleft=(1090, 107)),
                "x": 1090.0,
                "speed": 30
            },
                        {
                "image": self.cloud_2,
                "rect": self.cloud_2.get_rect(topleft=(866, 32)),
                "x": 866.0,
                "speed": 20
            },
                        {
                "image": self.cloud_3,
                "rect": self.cloud_3.get_rect(topleft=(616, 129)),
                "x": 616.0,
                "speed": 40
            },
                        {
                "image": self.cloud_4,
                "rect": self.cloud_4.get_rect(topleft=(340, 56)),
                "x": 340.0,
                "speed": 30
            }
        ]

        self.button_hovered = None
        self.button_pressed = None
        self.camera_rect = pygame.Rect(60, 420, 320, 240)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.button_hovered == "start":
                    self.button_pressed = "start"
                    print("start")
                elif self.button_hovered == "quit":
                    self.button_pressed = "quit"
                    print("quit")
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                self.button_pressed = None
            
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_choo_time:
            self.choo_choo.play()
            self.next_choo_time = (current_time + random.randint(5000, 10000))

        for cloud in self.clouds:
            cloud["x"] += cloud["speed"] / 60
            cloud["rect"].x = int(cloud["x"])

            if cloud["rect"].left > 1280:
                cloud["x"] = 440
                cloud["rect"].left = 440
        
        cursor_rect = pygame.Rect(
            self.cursor.position[0] - self.cursor.radius,
            self.cursor.position[1] - self.cursor.radius,
            self.cursor.radius * 2,
            self.cursor.radius * 2
        )

        if cursor_rect.colliderect(self.start_hitbox):
            self.button_hovered = "start"
        elif cursor_rect.colliderect(self.quit_hitbox):
            self.button_hovered = "quit"
        else:
            self.button_hovered = None

    def draw(self, screen):
        screen.fill((247, 248, 242))

        # background
        screen.blit(self.game_area, self.game_area_rect)

        # clouds
        for cloud in self.clouds:
            screen.blit(cloud["image"], cloud["rect"])

        # side panel
        screen.blit(self.side_panel, self.side_panel_rect)

        # static
        screen.blit(self.title, self.title_rect)
        screen.blit(self.high_score, self.high_score_rect)

        # button
        if self.button_pressed == "start":
            screen.blit(self.start_pressed_image, self.start_rect)
        elif self.button_hovered == "start":
            screen.blit(self.start_hovered_image, self.start_rect)
        else:
            screen.blit(self.start_image, self.start_rect)

        if self.button_pressed == "quit":
            screen.blit(self.quit_pressed_image, self.quit_rect)
        elif self.button_hovered == "quit":
            screen.blit(self.quit_hovered_image, self.quit_rect)
        else:
            screen.blit(self.quit_image, self.quit_rect)

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
