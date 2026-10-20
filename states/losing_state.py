import cv2
import pygame

from states.cursor import HandCursor


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

POPUP_WIDTH = 531
POPUP_HEIGHT = 452

POPUP_POSITION = (600, 136)

ORIGINAL_POPUP_SIZE = (872, 720)
ORIGINAL_BUTTON_SIZE = (305, 224)

HITBOX_OFFSET = (29, 97)
HITBOX_SIZE = (247, 99)


class LosingState:
    def __init__(self, camera, lower_hsv, upper_hsv, background):
        self.camera = camera
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv
        self.background = self.blur_background(background)

        self.cursor = HandCursor()
        self.next_state = None
        self.button_hovered = None
        self.button_pressed = None

        self.popup = pygame.image.load("assets/img/losing_screen.png").convert_alpha()
        self.popup = pygame.transform.smoothscale(self.popup, (POPUP_WIDTH, POPUP_HEIGHT))
        self.popup_rect = self.popup.get_rect(topleft=POPUP_POSITION)

        scale_x = POPUP_WIDTH / ORIGINAL_POPUP_SIZE[0]
        scale_y = POPUP_HEIGHT / ORIGINAL_POPUP_SIZE[1]
        button_size = (
            round(ORIGINAL_BUTTON_SIZE[0] * scale_x),
            round(ORIGINAL_BUTTON_SIZE[1] * scale_y)
        )

        self.buttons = {
            "restart": {
                "idle": self.load_button(
                    "assets/img/restart_idle.png",
                    button_size
                ),
                "hovered": self.load_button(
                    "assets/img/restart_hovered.png",
                    button_size
                ),
                "pressed": self.load_button(
                    "assets/img/restart_pressed.png",
                    button_size
                ),
            },
            "quit": {
                "idle": self.load_button(
                    "assets/img/quit2_idle.png",
                    button_size
                ),
                "hovered": self.load_button(
                    "assets/img/quit2_hovered.png",
                    button_size
                ),
                "pressed": self.load_button(
                    "assets/img/quit2_pressed.png",
                    button_size
                ),
            },
        }

        original_positions = {
            "restart": (90, 390),
            "quit": (480, 390),
        }

        self.button_positions = {
            name: (
                self.popup_rect.x + round(x * scale_x),
                self.popup_rect.y + round(y * scale_y)
            )
            for name, (x, y) in original_positions.items()
        }

        self.button_rects = {}
        self.button_hitboxes = {}

        for name, position in self.button_positions.items():
            image = self.buttons[name]["idle"]
            rect = image.get_rect(topleft=position)

            scale_x = image.get_width() / 305
            scale_y = image.get_height() / 224

            offset_x = round(HITBOX_OFFSET[0] * scale_x)
            offset_y = round(HITBOX_OFFSET[1] * scale_y)
            hitbox_width = round(HITBOX_SIZE[0] * scale_x)
            hitbox_height = round(HITBOX_SIZE[1] * scale_y)

            self.button_rects[name] = rect
            self.button_hitboxes[name] = pygame.Rect(
                rect.x + offset_x,
                rect.y + offset_y,
                hitbox_width,
                hitbox_height
            )

    @staticmethod
    def load_button(path, size):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, size)

    @staticmethod
    def blur_background(surface, blur_amount=21):
        frame = pygame.surfarray.array3d(surface)

        frame = cv2.transpose(frame)
        frame = cv2.GaussianBlur(frame, (blur_amount, blur_amount), 0)

        frame = cv2.transpose(frame)
        return pygame.surfarray.make_surface(frame)

    def handle_event(self, event):
        if self.next_state is not None:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.button_hovered == "restart":
                    self.button_pressed = "restart"
                    self.next_state = "restart"

                elif self.button_hovered == "quit":
                    self.button_pressed = "quit"
                    self.next_state = "menu"

    def update(self):
        if self.next_state is not None:
            return
        
        success, frame = self.camera.read()

        if success:
            frame = cv2.flip(frame, 1)
            hand_position = self.get_hand_position(frame)

            if hand_position is not None:
                self.cursor.update(hand_position)

        cursor_rect = pygame.Rect(
            self.cursor.position[0]
            - self.cursor.cursor.get_width() // 2,
            self.cursor.position[1]
            - self.cursor.cursor.get_height() // 2,
            self.cursor.cursor.get_width(),
            self.cursor.cursor.get_height()
        )

        self.button_hovered = None

        for name, hitbox in self.button_hitboxes.items():
            if cursor_rect.colliderect(hitbox):
                self.button_hovered = name
                break

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        screen.blit(self.popup, self.popup_rect)

        for name, rect in self.button_rects.items():
            if self.button_pressed == name:
                image = self.buttons[name]["pressed"]
            elif self.button_hovered == name:
                image = self.buttons[name]["hovered"]
            else:
                image = self.buttons[name]["idle"]

            screen.blit(image, rect)

        self.cursor.draw(screen)

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

        screen_x = int(hand_x / frame_width * WINDOW_WIDTH)
        screen_y = int(hand_y / frame_height * WINDOW_HEIGHT)

        return (screen_x, screen_y)