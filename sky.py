#!/usr/bin/env python3

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
        self.file = ""

    def sky_zone_set(self, zone_list: list[Any]) -> None:
        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0
        for zone in zone_list:
            try:
                if int(zone.xy[0]) > x_max:
                    x_max = int(zone.xy[0])
            except ValueError as e:
                print(e)
            try:
                if int(zone.xy[1]) > y_max:
                    y_max = int(zone.xy[1])
            except ValueError as e:
                print(e)
        for zone in zone_list:
            try:
                if int(zone.xy[0]) < x_min:
                    x_min = int(zone.xy[0])
            except ValueError as e:
                print(e)
            try:
                if int(zone.xy[1]) < y_min:
                    y_min = int(zone.xy[1])
            except ValueError as e:
                print(e)
        x_min = abs(x_min)
        y_min = abs(y_min)
        for zone in zone_list:
            try:
                zone.xy[0] = int(self.width / (x_max + 2 + x_min)) * \
                    (int(zone.xy[0]) + 1 + x_min)
            except ValueError as e:
                print(e)
            try:
                zone.xy[1] = int(self.height / (y_max + 2 + y_min)) * \
                    (int(zone.xy[1]) + 1 + y_min)
            except ValueError as e:
                print(e)

    def sky_draw_graph(
            self,
            zone_list: list[Any],
            screen: pygame.surface.Surface,
            connections: list[Any],
            dr_num: int 
            ) -> None:
        screen.fill(self.screen_color)
        text = pygame.font.SysFont("Impact", 32)
        id_text = text.render(("Drones: " + str(dr_num)), True, self.txt_color)
        screen.blit(id_text, (20, 20))
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
            try:
                pygame.draw.line(screen, "black", conn.xy1, conn.xy2, width=6)
                a = -3 + (conn.xy1[0] + conn.xy2[0]) / 2
                b = -6 + (conn.xy1[1] + conn.xy2[1]) / 2
                screen.blit(id_text, (a, b))
            except TypeError as e:
                print(e)
        for zone in zone_list:
            text = pygame.font.SysFont("Impact", 18)
            txt_pos = (zone.xy[0], zone.xy[1])
            if zone.color == "rainbow":
                zone.color = "violet"
            try:
                pygame.draw.circle(screen, zone.color, txt_pos, zone.radius)
            except (TypeError, ValueError) as e:
                print(e)
            if "_" in zone.name:
                z_name = zone.name.split("_", 1)
                id_text = text.render(
                    z_name[0].capitalize(), True, self.txt_color
                    )
                screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 50))
                id_text = text.render(z_name[1], True, self.txt_color)
                screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 37))
            else:
                id_text = text.render(
                    zone.name.capitalize(), True, self.txt_color
                    )
                try:
                    screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 40))
                except TypeError as e:
                    print(e)
            id_text = text.render(zone.max_drones, True, "black")
            try:
                screen.blit(id_text, (zone.xy[0] - 5, zone.xy[1] - 5))
            except TypeError as e:
                print(e)
            if zone.priority == "priority":
                id_text = text.render("P", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 5))
            if zone.priority == "restricted":
                id_text = text.render("X", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 5))

    def drone_fly(
            self,
            a: list[float],
            b: list[float],
            drone: drone_factory,
            screen: pygame.surface.Surface
            ) -> list[float]:
        try:
            start = pygame.Vector2(a[0], a[1])
            target = pygame.Vector2(b[0], b[1])
            direction = target - start
            position = (start.x - 4, start.y - 6)
            pygame.draw.circle(
                screen,
                drone.drone_color,
                start,
                drone.drone_radius
                )
            screen.blit(drone.id_rend, position)
            if direction.length() > 1:
                direction = direction.normalize()
                start = pygame.Vector2(start + direction * 1.2)
            return [start[0], start[1]]
        except (ValueError, UnboundLocalError) as e:
            print(e)
            exit()

    def path_finder(self,
            zone_list: list[Any],
            connections: list[Any]
            ) -> list[Any]:
        hub_list: list[Any] = []
        temp1 = []
        temp2 = []
        for conn in connections:
            for zone in zone_list:
                if zone.name == conn.name1:
                    temp1 = zone.xy
                if zone.name == conn.name2:
                    temp2 = zone.xy
                
            hub_list.append([temp1, temp2])

        return hub_list

    def sky_build(
            self,
            zone_list: list[Any],
            drone_list: list[Any],
            connections: list[Any]
            ) -> None:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((self.width, self.height))
        phase = "drone_fly"
        self.sky_zone_set(zone_list)
        screen_background = pygame.Surface((self.width, self.height))
        drone_number = len(drone_list)
        self.sky_draw_graph(
            zone_list, screen_background, connections, drone_number
            )
        dr_iter = iter(drone_list)
        drone = next(dr_iter)
        hub_list = self.path_finder(zone_list, connections)
        hub_iter = iter(hub_list)
        path = next(hub_iter)
        start = path[0]
        target = path[1]

        hub_list = self.path_finder(zone_list, connections)
        print(hub_list)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                break
            if keys[pygame.K_q]:
                break
            screen.blit(screen_background, (0, 0))
            start = self.drone_fly(start, target, drone, screen)
            if (abs(start[0] - target[0]) + abs(start[1] - target[1]) < 2)\
                and phase == "drone_fly":
                try:
                    temp = next(hub_iter)
                    start = temp[0]
                    target = temp[1]
                except StopIteration:
                    phase = "drone_change"
            if phase == "drone_change":
                try:
                    drone = next(dr_iter)
                    hub_iter = iter(hub_list)
                    path = next(hub_iter)
                    start = path[0]
                    target = path[1]
                    phase = "drone_fly"
                except StopIteration:
                    phase = "drone_rest"
            pygame.display.flip()
