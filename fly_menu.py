#!/usr/bin/env python3

from pydantic import ValidationError
from typing import Any
import pygame
from pathlib import Path
from sky import sky

class menu(sky):
    def __init__(
            self,
            input: str,
            index: dict[str, list[str]] = {}
            ) -> None:
        self.index = index
        self.input = input

    def menu_sky(self) -> None:
        path = Path(self.input)
        files: list[str] = []
        index: dict[str, list[str]] = {}
        dirs = [d.name for d in path.iterdir() if d.is_dir()]
        for director in dirs:
            filepath = f"{path}/{director}"
            files = [d.name for d in Path(filepath).iterdir() if d.is_file()]
            index.update({director: files})
        self.index = index

    def menu_build(self, width, height) -> None:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((width, height))
        text = pygame.font.SysFont("Arial", 30)
        running = True
        span = self.menu_zone_set(width, height)
        oriz = span[1]
        vert = span[0]
        while running:
            x = -200
            y = 0
            rectangle = pygame.Rect(80 + y, 300 + x, 300, 80)
            cur = [rectangle.x, rectangle.y]
            for key, value in self.index.items():
                pygame.draw.rect(screen, "white", rectangle, width=4)
                id_text = text.render(key.capitalize(), True, "white")
                text_rect = id_text.get_rect(center=rectangle.center)
                screen.blit(id_text, text_rect)
                back_y = rectangle.y
                for elem in value:
                    rectangle.y += vert
                    elem = elem[3:-4].capitalize()
                    elem = elem.replace("_", " ")
                    if cur[0] == rectangle.x and cur[1] == rectangle.y:
                        color = "red"
                    else:
                        color = "white"
                    pygame.draw.rect(screen, color, rectangle, width=4)
                    id_text = text.render(elem, True, "white")
                    text_rect = id_text.get_rect(center=rectangle.center)
                    screen.blit(id_text, text_rect)
                rectangle.x += oriz
                rectangle.y = back_y
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                break
            if keys[pygame.K_q]:
                exit()
            pygame.display.flip()

    def menu_zone_set(self, width, height) -> list[int]:
        x_max = 0
        y_max = 0
        x_max = len(self.index)
        for _, value in self.index.items():
            if len(value) > y_max:
                y_max = len(value)
        span = [(int(height / (x_max + 1))), (int(width / (y_max + 1)))]
        return span
