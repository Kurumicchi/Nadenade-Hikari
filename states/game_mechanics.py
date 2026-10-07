import random
import pygame

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
        self.health = 3

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

        x = (
            self.game_area_rect.x
            + padding_x
            + column * (cell_width + gap)
        )

        y = (
            self.game_area_rect.y
            + padding_y
            + row * (cell_height + gap)
        )

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

            if state != self.EMPTY:
                font = pygame.font.Font(None, 32)

                text = font.render(
                    cell["character"].upper(),
                    True,
                    (40, 40, 40)
                )

                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)


    def click(self, position):
        for index, cell in enumerate(self.cells):
            if cell["state"] != self.ACTIVE:
                continue

            rect = self.get_cell_rect(index)

            if not rect.collidepoint(position):
                continue

            if cell["character"] == "hikari":
                cell["state"] = self.HIT
                cell["timer"] = 0

                self.score += 100
                print(f"Hit Hikari! Score: {self.score}")

            elif cell["character"] == "nozomi":
                cell["state"] = self.MISS
                cell["timer"] = 0

                self.health -= 1
                print(f"Hit Nozomi! Health: {self.health}")

            return