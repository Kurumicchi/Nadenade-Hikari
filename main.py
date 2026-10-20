import cv2
import json
import pygame

from states.menu_state import MenuState
from states.game_state import GameState
from states.losing_state import LosingState

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def load_calibration():
    with open("calibration.json", "r") as file:
        data = json.load(file)

    lower_hsv = tuple(data["lower_hsv"])
    upper_hsv = tuple(data["upper_hsv"])

    return lower_hsv, upper_hsv

def create_menu_state(camera, lower_hsv, upper_hsv):
    return MenuState(camera, lower_hsv, upper_hsv)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nadenade Hikari")

    lower_hsv, upper_hsv = load_calibration()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return

    current_state = GameState(
        camera,
        lower_hsv,
        upper_hsv
    )
    clock = pygame.time.Clock()
    running = True


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            current_state.handle_event(event)

        if not running:
            break

        current_state.update()
        current_state.draw(screen)

        pygame.display.flip()

        next_state = current_state.next_state

        if next_state == "game":
            current_state = GameState(
                camera,
                lower_hsv,
                upper_hsv
            )

        elif next_state == "menu":
            current_state = create_menu_state(
                camera,
                lower_hsv,
                upper_hsv
            )

        elif next_state == "losing":
            background = screen.copy()

            current_state = LosingState(
                camera,
                lower_hsv,
                upper_hsv,
                background
            )

        elif next_state == "restart":
            current_state = GameState(
                camera,
                lower_hsv,
                upper_hsv
            )

        elif next_state == "quit":
            running = False

        clock.tick(60)

    camera.release()
    cv2.destroyAllWindows()
    pygame.quit()

if __name__ == "__main__":
    main()