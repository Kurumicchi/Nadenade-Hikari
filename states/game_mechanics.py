import random
import pygame
from high_score import load_high_score, save_high_score

class GameMechanics:
    EMPTY = "empty"
    APPEARING = "appearing"
    ACTIVE = "active"
    LEAVING = "leaving"
    HIT = "hit"
    MISS = "miss"

    def __init__(self, game_area_rect):
        self.game_area_rect = game_area_rect

        self.score = 0
        self.health = 1
        self.high_score_saved = False

        self.score_per_hit = 100
        self.score_popup = []
        self.score_popup_font = pygame.font.Font("assets/font/Fredoka-Bold.ttf", 36)
        self.score_popup_duration = 700

        self.rows = 3
        self.columns = 5

        self.cells = [
            {
                "state": self.EMPTY,
                "character": None,
                "timer": 0
            }
            for _ in range(self.rows * self.columns)
        ]

        self.appear_duration = 500
        self.active_duration = 2000
        self.leave_duration = 500
        self.hit_duration = 500
        self.miss_duration = 500

        self.game_timer = 0
        self.spawn_timer = 0
        self.spawn_interval = 2500
        
        self.spawn_character()

    def spawn_character(self):
        empty_cells = [
            index
            for index, cell in enumerate(self.cells)
            if cell["state"] == self.EMPTY
        ]

        if not empty_cells:
            return

        cell_index = random.choice(empty_cells)
        cell = self.cells[cell_index]

        cell["state"] = self.APPEARING
        cell["character"] = random.choice([
            "hikari",
            "nozomi"
        ])
        cell["timer"] = 0

    def update(self, delta_time):
        # timer
        self.game_timer += delta_time
        self.spawn_timer += delta_time

        if self.game_timer >= 100000:
            self.spawn_interval = 800

        elif self.game_timer >= 80000:
            self.spawn_interval = 1000

        elif self.game_timer >= 60000:
            self.spawn_interval = 1200

        elif self.game_timer >= 40000:
            self.spawn_interval = 1500

        elif self.game_timer >= 20000:
            self.spawn_interval = 1800

        else:
            self.spawn_interval = 2500

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_character()
            self.spawn_timer = 0

        # cells
        for cell in self.cells:
            if cell["state"] == self.EMPTY:
                continue

            cell["timer"] += delta_time

            if cell["state"] == self.APPEARING:
                if cell["timer"] >= self.appear_duration:
                    cell["state"] = self.ACTIVE
                    cell["timer"] = 0

            elif cell["state"] == self.ACTIVE:
                if cell["timer"] >= self.active_duration:
                    cell["state"] = self.LEAVING
                    cell["timer"] = 0

            elif cell["state"] == self.LEAVING:
                if cell["timer"] >= self.leave_duration:
                    cell["state"] = self.EMPTY
                    cell["character"] = None
                    cell["timer"] = 0

            elif cell["state"] == self.HIT:
                if cell["timer"] >= self.hit_duration:
                    cell["state"] = self.EMPTY
                    cell["character"] = None
                    cell["timer"] = 0

            elif cell["state"] == self.MISS:
                if cell["timer"] >= self.miss_duration:
                    cell["state"] = self.EMPTY
                    cell["character"] = None
                    cell["timer"] = 0

        # popup
        for popup in self.score_popup:
            popup["timer"] -= delta_time
            popup["y"] -= 0.05 * delta_time

        self.score_popup = [
            popup for popup in self.score_popup
            if popup["timer"] > 0
        ]

        # highscore
        self.save_high_score_if_needed()

    # placeholder
    def get_cell_rect(self, index):
        padding_x = 40
        padding_y = 45
        gap = 10

        grid_width = self.game_area_rect.width - padding_x * 2
        grid_height = self.game_area_rect.height - padding_y * 2

        cell_width = (
            grid_width - gap * (self.columns - 1)
        ) // self.columns

        cell_height = (
            grid_height - gap * (self.rows - 1)
        ) // self.rows

        column = index % self.columns
        row = index // self.columns

        x = padding_x + column * (cell_width + gap)

        y = padding_y + row * (cell_height + gap)

        return pygame.Rect(
            x,
            y,
            cell_width,
            cell_height
        )

    # placeholder
    def draw(self, screen):
        for index, cell in enumerate(self.cells):
            rect = self.get_cell_rect(index)
            state = cell["state"]

            if state == self.EMPTY:
                color = (220, 220, 220) # gray

            elif state == self.APPEARING:
                color = (180, 220, 180) # light green

            elif state == self.ACTIVE:
                color = (120, 220, 150) # green

            elif state ==self.HIT:
                color = (255, 220, 80) # yellow

            elif state == self.MISS:
                color = (220, 100, 100) # red

            else:
                color = (220, 180, 180) # light red

            pygame.draw.rect(screen, color, rect)

            pygame.draw.rect(
                screen,
                (40, 40, 40),
                rect,
                width=2
            )

            if state == self.ACTIVE:
                font = pygame.font.Font(None, 32)

                text = font.render(
                    cell["character"].upper(),
                    True,
                    (40, 40, 40)
                )

                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        self.draw_score_popup(screen)

    def click(self, position):
        for index, cell in enumerate(self.cells):
            if cell["state"] != self.ACTIVE:
                continue

            rect = self.get_cell_rect(index)

            local_position = (
                position[0] - self.game_area_rect.x,
                position[1] - self.game_area_rect.y
            )

            if not rect.collidepoint(local_position):
                continue

            if cell["character"] == "hikari":
                cell["state"] = self.HIT
                cell["timer"] = 0

                self.score += self.score_per_hit
                # print(f"Hit Hikari! Score: {self.score}")

                self.score_popup.append({
                    "x": rect.centerx,
                    "y": rect.top - 10,
                    "timer": self.score_popup_duration
                })

            elif cell["character"] == "nozomi":
                cell["state"] = self.MISS
                cell["timer"] = 0

                self.health -= 1
                #print(f"Hit Nozomi! Health: {self.health}")

            return

    def draw_score_popup(self, surface):
        outline_color = (66, 49, 77)
        text_color = (255, 249, 222)
        outline_width = 2

        for popup in self.score_popup:
            progress = popup["timer"] / self.score_popup_duration
            alpha = int(255 * progress)

            score_text = self.score_popup_font.render(
                "+100", True, text_color
            )

            outline = self.score_popup_font.render(
                "+100", True, outline_color
            )

            score_text.set_alpha(alpha)
            outline.set_alpha(alpha)

            text_rect = score_text.get_rect(
                center=(int(popup["x"]), int(popup["y"]))
            )

            for dx in range(-outline_width, outline_width + 1):
                for dy in range(-outline_width, outline_width + 1):
                    if dx * dx + dy * dy <= outline_width * outline_width:
                        outline_rect = text_rect.move(dx, dy)
                        surface.blit(outline, outline_rect)

            surface.blit(score_text, text_rect)

    def save_high_score_if_needed(self):
        if self.high_score_saved or self.health > 0:
            return

        current_high_score = load_high_score()

        if self.score > current_high_score:
            save_high_score(self.score)
            print(f"New high score: {self.score}")

        self.high_score_saved = True