#!/usr/bin/env python3

import pygame
from typing import Any, Iterator
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
        self.text_color = "gray"
        self.border_color = "gray"
        self.selected_color = "red"
        self.border_width = 8
        self.oriz = 0
        self.vert = 0

    def menu_file_mapping(self) -> None:
        """Analize the given directory, searching txt files
        in all subdirectories, creating a dictionary in self.index
        """
        path = Path(self.input)
        files: list[str] = []
        index: dict[str, list[str]] = {}
        dirs = [d.name for d in path.iterdir() if d.is_dir()]
        for director in dirs:
            filepath = f"{path}/{director}"
            files = [d.name for d in Path(filepath).iterdir() if d.is_file()]
            index.update({director: files})
        self.index = index

    def menu_builder(self, width: int, height: int) -> None:
        """Create the concrete pygame interactive menu"""
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((width, height))
        screen.fill((0, 90, 90))
        running = True
        difficulty = "easy"
        file = "01_linear_path.txt"
        files = []
        files_list: Iterator[Any] = iter([])
        flag = ""
        while running:
            text = pygame.font.SysFont("Arial", 20)
            x = 0
            y = 0
            rectangle = pygame.Rect(50 + y, 300 + x, 250, 80)
            for key, value in self.index.items():
                if difficulty == key:
                    color = self.selected_color
                    files = value
                else:
                    color = self.border_color
                pygame.draw.rect(
                    screen, color, rectangle, width=self.border_width
                    )
                id_text = text.render(key.capitalize(), True, self.text_color)
                text_rect = id_text.get_rect(center=rectangle.center)
                screen.blit(id_text, text_rect)
                back_y = rectangle.y
                for elem in value:
                    rectangle.y += self.vert
                    if file == elem:
                        color = self.selected_color
                    else:
                        color = self.border_color
                    elem = elem[3:-4].capitalize()
                    elem = elem.replace("_", " ")
                    pygame.draw.rect(
                        screen, color, rectangle, width=self.border_width
                        )
                    id_text = text.render(elem, True, self.text_color)
                    text_rect = id_text.get_rect(center=rectangle.center)
                    screen.blit(id_text, text_rect)
                rectangle.x += self.oriz
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
            pygame.draw.rect(screen, "gray", title, width=self.border_width)
            text = pygame.font.SysFont("Arial", 35)
            id_text = text.render(
                "Press 'D' to change difficulty - Press 'F' to change map - "
                "Press 'P' to flip menu/graph - "
                "Press 'Q' to quit", True, self.text_color)
            text_rect = id_text.get_rect(center=title.center)
            screen.blit(id_text, text_rect)
            pygame.display.flip()

    def menu_zone_set(self, width: int, height: int) -> None:
        """Calculate vertical and orizontal spanning in order to display
        variable menu elements, it function with not too much elements
        """
        x_max = 0
        y_max = 0
        x_max = len(self.index)
        for _, value in self.index.items():
            if len(value) > y_max:
                y_max = len(value)
        self.oriz = (int(width / (y_max + 3)))
        self.vert = (int(height / (x_max + 2)))
