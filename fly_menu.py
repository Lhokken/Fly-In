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
        self.iter_index = iter(self.index)
        self.file_path = "null"

    def menu_sky(self) -> None:
        path = Path(self.input)
        files: list[str] = []
        index: dict[str, list[str]] = {}
        dirs = [d.name for d in path.iterdir() if d.is_dir()]
        for director in dirs:
            filepath = f"{path}/{director}"
            files = [d.name for d in Path(filepath).iterdir() if d.is_file()]
            index.update({director: files})
            print(index)
        self.index = index

    def menu_build(self, width, height) -> None:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((width, height))
        running = True
        span = self.menu_zone_set(width, height)
        oriz = span[0]
        vert = span[1]
        difficulty = "easy"
        file = "01_linear_path.txt"
        files = []
        files_list = iter([])
        flag = ""
        while running:
            text = pygame.font.SysFont("Arial", 20)
            x = 0
            y = 0
            rectangle = pygame.Rect(50 + y, 250 + x, 250, 80)
            for key, value in self.index.items():
                if difficulty == key:
                    color = "red"
                    files = value
                else:
                    color = "gray"
                pygame.draw.rect(screen, color, rectangle, width=4)
                id_text = text.render(key.capitalize(), True, "gray")
                text_rect = id_text.get_rect(center=rectangle.center)
                screen.blit(id_text, text_rect)
                back_y = rectangle.y
                for elem in value:
                    rectangle.y += vert
                    if file == elem:
                        color = "red"
                    else:
                        color = "gray"
                    elem = elem[3:-4].capitalize()
                    elem = elem.replace("_", " ")
                    pygame.draw.rect(screen, color, rectangle, width=4)
                    id_text = text.render(elem, True, "gray")
                    text_rect = id_text.get_rect(center=rectangle.center)
                    screen.blit(id_text, text_rect)
                rectangle.x += oriz
                rectangle.y = back_y
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return
                    if event.key == pygame.K_q:
                        exit()
                    if event.key == pygame.K_d:
                        flag = "change"
                        try:
                            difficulty = next(self.iter_index)
                        except StopIteration:
                            self.iter_index = iter(self.index)
                            difficulty = next(self.iter_index)
                    if event.key == pygame.K_f:
                        if flag == "change":
                            files_list = iter(files)
                            flag = ""
                        try:
                            file = next(files_list)
                            self.file_path = "maps/" + difficulty + "/" + file
                        except StopIteration:
                            files_list = iter(files)
            title = pygame.Rect(50, 50, width - 200, 170)
            pygame.draw.rect(screen, "gray", title, width=4)
            text = pygame.font.SysFont("Arial", 35)
            id_text = text.render(
                "Press 'D' to change difficulty - Press 'F' to change map - "
                "Press 'P' to flip menu/graph - Press 'Q' to quit", True, "gray")
            text_rect = id_text.get_rect(center=title.center)
            screen.blit(id_text, text_rect)
            pygame.display.flip()

    def menu_zone_set(self, width, height) -> list[int]:
        x_max = 0
        y_max = 0
        x_max = len(self.index)
        for _, value in self.index.items():
            if len(value) > y_max:
                y_max = len(value)
        span = [(int(width / (y_max + 3))), (int(height / (x_max + 2)))]
        return span
