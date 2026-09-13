import cv2
import json
import pygame

from states.menu_state import menu_state

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

def load_calibration():
    with open("calibration.json", "r") as file:
        data = json.load(file)

    lower_hsv = tuple(data["lower_hsv"])
    upper_hsv = tuple(data["upper_hsv"])

    return lower_hsv, upper_hsv

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Nadenade Hikari")

    lower_hsv, upper_hsv = load_calibration()

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open camera.")
        return

    current_state = menu_state(
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

            current_state.handle_event(event)

        current_state.update()
        current_state.draw(screen)

        pygame.display.flip()
        clock.tick(60)



    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()