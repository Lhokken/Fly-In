#!/usr/bin/env python3

from typing import Any
import pygame


class Validation_graph(Exception):

    @classmethod
    def validate_parts(cls, parts: Any) -> bool:
        temp = parts[0].replace(" ", "")
        temp = temp.replace("-", "")
        if len(temp) != len(parts[0]):
            cls.data_error("No \" \" or \"-\" in zones names")
            return False
        try:
            _ = int(parts[1])
            _ = int(parts[2])
        except ValueError:
            cls.data_error("Coordinates must be integer > 0")
            return False
        return True

    @classmethod
    def validate_conn(cls, temp: list[str], hubs: dict[Any, Any]) -> bool:
        zones = list(hubs.keys())
        if temp[0] not in zones or temp[1].split(" ")[0] not in zones:
            cls.data_error("Connection to unknown zone")
            return False

        return True

    @classmethod
    def validate_conn_dup(cls, connections: list[Any]) -> bool:
        for temp in connections:
            rev = temp[::-1]
            for conn in connections:
                if conn == rev:
                    cls.data_error("Error: duplicate connections")
                    return False
        return True

    @classmethod
    def valid_conn_meta(cls, data: dict[Any, Any]) -> bool:
        if data[0] == "[" and data[-1] == "]" and "=" in data:
            return True
        cls.data_error("Syntax error in metadata")
        return False

    @classmethod
    def valid_conn_link(cls, max_link_cap: int) -> bool:
        print("--", max_link_cap)
        if max_link_cap != "" and int(max_link_cap) < 0:
            return False
        return True

    @classmethod
    def validation_zone(cls, zone_list: list[Any]) -> bool:
        for zone in zone_list:
            if zone.priority not in (
                'normal', 'blocked', 'restricted', 'priority'):
                cls.data_error("Unknown zone name")
                return False
            if zone.max_drones is not None and int(zone.max_drones) < 0:
                cls.data_error("Max drones must be positive integer")
                return False
        return True

    @classmethod
    def data_error(cls, message: str) -> None:
        screen = pygame.display.set_mode((1000, 400))
        title = pygame.Rect(10, 10, 980, 380)
        offset_y = title.top + 80
        pygame.draw.rect(screen, "gray", title, width=4)
        text = pygame.font.SysFont("Arial", 35)
        id_text = text.render(message, True, "gray")
        text_rect = id_text.get_rect(midtop=(title.centerx, offset_y))
        screen.blit(id_text, text_rect)
        offset_y = offset_y + 180
        id_text = text.render("Press C to continue", True, "gray")
        text_rect = id_text.get_rect(midtop=(title.centerx, offset_y))
        screen.blit(id_text, text_rect)
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_c]:
                break
