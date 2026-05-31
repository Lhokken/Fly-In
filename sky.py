#!/usr/bin/env python3

from pydantic import ValidationError
from typing import Any
from fly_in import drone_factory
import pygame


class sky():
    def __init__(
            self,
            height: int = 900,
            widht: int = 1900,
            txt_color: str = "White",
            screen_color: tuple[int, int, int] = (0, 180, 180),
            ) -> None:
        pygame.init()
        pygame.font.init()
        self.height = height
        self.width = widht
        self.txt_color = txt_color
        self.screen_color = screen_color
        self.id_txt = pygame.font.SysFont("Impact", 18)
        self.clock = pygame.time.Clock()

    def sky_zone_set(self, zone_list: list[Any]) -> None:
        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0
        for zone in zone_list:
            if int(zone.xy[0]) > x_max:
                x_max = int(zone.xy[0])
            if int(zone.xy[1]) > y_max:
                y_max = int(zone.xy[1])
        for zone in zone_list:
            if int(zone.xy[0]) < x_min:
                x_min = int(zone.xy[0])
            if int(zone.xy[1]) < y_min:
                y_min = int(zone.xy[1])
        x_min = abs(x_min)
        y_min = abs(y_min)
        for zone in zone_list:
            zone.xy[0] = int(self.width / (x_max + 2 + x_min)) * \
                (int(zone.xy[0]) + 1 + x_min)
            zone.xy[1] = int(self.height / (y_max + 2 + y_min)) * \
                (int(zone.xy[1]) + 1 + y_min)

    def sky_draw_graph(
            self,
            zone_list: list[Any],
            screen: pygame.surface.Surface,
            connections: list[Any]
            ) -> None:
        screen.fill(self.screen_color)
        for conn in connections:
            for zone in zone_list:
                if conn.name1 == zone.name:
                    conn.xy1 = zone.xy
                if conn.name2 == zone.name:
                    conn.xy2 = zone.xy
            txt_pos = (conn.xy1, conn.xy2)
            text = pygame.font.SysFont("Impact", 22)
            id_text = text.render(
                str(conn.max_link_capacity), True, self.txt_color
                )
            pygame.draw.line(screen, "black", conn.xy1, conn.xy2, width=6)
            a = -3 + (conn.xy1[0] + conn.xy2[0]) / 2
            b = -6 + (conn.xy1[1] + conn.xy2[1]) / 2
            screen.blit(id_text, (a, b))
        for zone in zone_list:
            text = pygame.font.SysFont("Impact", 16)
            txt_pos = (zone.xy[0], zone.xy[1])
            id_text = text.render(zone.name.capitalize(), True, self.txt_color)
            pygame.draw.circle(screen, zone.color, txt_pos, zone.radius)
            screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 50))
            id_text = text.render(zone.max_drones, True, "black")
            screen.blit(id_text, (zone.xy[0] - 5, zone.xy[1] - 5))
            if zone.priority == "priority":
                id_text = text.render("P", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 5))
            if zone.priority == "restricted":
                id_text = text.render("X", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 5))

    def drone_fly(
            self,
            a: list[int],
            b: list[int],
            drone: drone_factory,
            screen: pygame.surface.Surface,
            dt: float
            ) -> list[int]:
        start = pygame.Vector2(a[0], a[1])
        target = pygame.Vector2(b[0], b[0])
        direction = target - start
        txt_pos = (start.x - 4, start.y - 6)
        pygame.draw.circle(
            screen,
            drone.drone_color,
            start,
            drone.drone_radius
            )
        screen.blit(drone.id_rend, txt_pos)
        direction = target - start
        if direction.length() > 5:
            direction = direction.normalize()
            start = pygame.Vector2(start + direction * 300 * dt)
        pygame.display.flip()
        return [int(start[0]), int(start[1])]

    def sky_build(
            self,
            zone_list: list[Any],
            drone_list: list[Any],
            connections: list[Any]
            ) -> None:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = self.clock
        dt: float = 0
        running = True
        start = [50, 50]
        target = [400, 1700]
        self.sky_zone_set(zone_list)
        drone = drone_list[0]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                break
            if keys[pygame.K_q]:
                break
            self.sky_draw_graph(zone_list, screen, connections)
            start = self.drone_fly(start, target, drone, screen, dt)
            dt = (clock.tick(60) / 1000)
            pygame.display.flip()
