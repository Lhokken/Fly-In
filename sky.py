#!/usr/bin/env python3

from typing import Any
from collections.abc import Generator
from fly_in import drone_factory
import pygame
import random
from fly_in import zone_factory as zone
from fly_in import drone_factory as drone
from fly_in import connection_factory as connections

color_set = {
    "white",
    "red",
    "green",
    "blue",
    "yellow",
    "magenta",
    "cyan"
}

def ft_color_randomizer() -> Generator:
        while True:
            for color in color_set:
                yield(color)

color_randomizer = ft_color_randomizer()

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

    def sky_zone_set(self, zone_list: list[zone]) -> None:
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
            zone_list: list[zone],
            screen: pygame.surface.Surface,
            connections: list[connections],
            dr_num: int 
            ) -> None:
        screen.fill(self.screen_color)
        text = pygame.font.SysFont("Impact", 32)
        id_text = text.render((
            f"Drones: {str(dr_num)} >-< Priority: P "
             ">-< Restricted: X >-< Blocked: B"
            ), True, self.txt_color)
        
        screen.blit(id_text, (20, 20))
        for conn in connections:
            for zone in zone_list:
                if conn.name1 == zone.name:
                    conn.xy1 = zone.xy
                if conn.name2 == zone.name:
                    conn.xy2 = zone.xy
            txt_pos = (conn.xy1, conn.xy2)
            text = pygame.font.SysFont("Impact", 22)
            # id_text = text.render(
            #     str(conn.max_link_capacity), True, self.txt_color
            #     )
            conn.park = [
                ((conn.xy1[0] + conn.xy2[0]) / 2),
                ((conn.xy1[1] + conn.xy2[1]) / 2)
                ]
            id_text = text.render(
                str(conn.max_link_capacity), True, self.txt_color
                )
            try:
                pygame.draw.line(screen, "black", conn.xy1, conn.xy2, width=6)
                a = -3 + conn.park[0]
                b = -6 + conn.park[1]
                screen.blit(id_text, (a, b))
            except TypeError as e:
                print(e)
        for zone in zone_list:
            text = pygame.font.SysFont("Impact", 18)
            drn_pos = (zone.xy[0], zone.xy[1])
            random_color = next(color_randomizer)
            if zone.color == "rainbow":
                zone.color = random_color
            if zone.color == "black":
                zone.color = (70, 70, 70)
            try:
                pygame.draw.circle(screen, zone.color, drn_pos, zone.radius)
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
            id_text = text.render(str(zone.max_drones), True, "black")
            try:
                screen.blit(id_text, (zone.xy[0] - 15, zone.xy[1] - 5))
            except TypeError as e:
                print(e)
            if zone.priority == "priority":
                id_text = text.render("P", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 15))
            if zone.priority == "restricted":
                id_text = text.render("X", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 15))
            if zone.priority == "blocked":
                id_text = text.render("B", True, "black")
                screen.blit(id_text, (zone.xy[0] + 5, zone.xy[1] - 15))

    def drone_fly_draw(self, drone, screen, direction, place) -> None:
        enlarger = 0
        if direction.length() < 65 and direction.length() > 15:
            enlarger = 10
        pos = (place.x , place.y)
        position = (place.x - 4, place.y - 6)
        pygame.draw.circle(
            screen,
            drone.drone_color,
            pos,
            drone.drone_radius + enlarger
            )
        screen.blit(drone.id_rend, position)

    def drone_fly(
            self,
            line_sim: list[drone],
            screen: pygame.surface.Surface,
            screen_background: pygame.surface.Surface
            ) -> None:
        for i in range(0, len(line_sim)):
            try:
                dron = line_sim[i]
                if not dron.start == None:
                    dron.place = pygame.Vector2(dron.start[0], dron.start[1])
                if not dron.target == None:
                    dron.target = pygame.Vector2(dron.target[0], dron.target[1])
            except (TypeError, IndexError):
                return
            while True:
                try:
                    screen.blit(screen_background, (0, 0))
                    if not dron.target == None and not dron.place == None:
                        dron.direction = dron.target - dron.place
                    self.drone_fly_draw(dron, screen, dron.direction, dron.place)
                    pygame.display.flip()
                    if not dron.direction == None\
                        and not dron.place == None\
                        and dron.direction.length() > 1:
                        dron.direction = dron.direction.normalize()
                        dron.place = pygame.Vector2(dron.place + dron.direction * 1.8)
                    elif not dron.place == None:
                        dron.start = pygame.Vector2(dron.place[0], dron.place[1])
                        try:
                            dron.target = pygame.Vector2(*next(dron.way))
                            # return
                        except StopIteration:
                            line_sim.pop(0)
                            return
                except (ValueError, UnboundLocalError) as e:
                    print(e)
                    exit()

    def zone_connections(
            self,
            zone_list: list[Any],
            connections: list[Any]
            ) -> None:
        for zone in zone_list:
            for conn in connections:
                if zone.name == conn.name1 or zone.name == conn.name2:
                    zone.link.append([conn.name1, conn.name2])

    def zone_cost(self, zone) -> int:
        cost: int = 0
        if zone.priority == "normal":
            cost = 1
        if zone.priority == "blocked":
            cost = 500000
        if zone.priority == "restricted":
            cost = 2
        if zone.priority == "priority":
            cost = 1
        return cost

    def path_finder(self,
            zone_list: list[zone],
            connections: list[connections]
            ) -> list[Any]:
        curr_hub: list[Any] = []
        temp_hub: list[Any] = []
        path: list[Any] = []
        # normal: Standard zone with cost 1 (default)
        # blocked: Inaccessible zone. Any path using it is invalid.
        # restricted: A sensitive or dangerous zone. Costs 2.
        # priority: A preferred zone. Costs 1 turn but is prioritized.
        self.zone_connections(zone_list, connections)
        curr_hub.append(zone_list[0])
        curr_hub[0].check = "visited"
        curr_hub[0].cost = 0
        check = True
        while check:
            for hub in curr_hub:
                if hub.type == "end_hub":
                    check = False
            for hub in curr_hub:
                for conn in hub.link:
                    for zone in zone_list:
                        if zone.name == conn[1] and zone.checked is False:
                            if zone.priority == "blocked":
                                continue
                            elif zone.priority == "priority":
                                zone.previous = conn[0]
                                zone.cost = 1 + hub.cost
                                zone.checked = True
                                temp_hub.append(zone)
                            elif zone.priority == "restricted":
                                if zone.pause is True:
                                    zone.previous = conn[0]
                                    zone.cost = 1 + hub.cost
                                    zone.checked = True
                                    zone.pause = False
                                    temp_hub.append(zone)
                                elif zone.pause is False:
                                    zone.cost = 1 + hub.cost
                                    zone.pause = True
                                    temp_hub.append(hub)
                            else:
                                zone.previous = conn[0]
                                zone.cost = 1 + hub.cost
                                zone.checked = True
                                temp_hub.append(zone)
            curr_hub = []
            curr_hub = temp_hub
            temp_hub = []
        zone_dict = {}
        zone_dict = {
            zone.name: zone for zone in zone_list if (
                not zone.previous == [] and not zone is None
                )
                }
        curr = zone_list[-1]
        path.append(curr.xy)
        while True:
            next = zone_dict.get(str(curr.previous))
            if next is None:
                path.append(zone_list[0].xy)
                break
            path.append(next.xy)
            curr = next
        return path[::-1]

    def sky_build(
            self,
            zone_list: list[zone],
            drone_list: list[drone],
            connections: list[connections]
            ) -> None:
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((self.width, self.height))
        self.sky_zone_set(zone_list)
        screen_background = pygame.Surface((self.width, self.height))
        self.sky_draw_graph(
            zone_list, screen_background, connections, len(drone_list)
            )

        hub_list = self.path_finder(zone_list, connections)

        for drone in drone_list:
            drone.start = pygame.Vector2(hub_list[0][0], hub_list[0][1])
            drone.target = pygame.Vector2(hub_list[1][0], hub_list[1][1])
            drone.way = iter(hub_list[2:])

        line_iter = iter(drone_list)
        line_sim = []
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
            try:
                line_sim.append(next(line_iter))
            except StopIteration:
                pass
            self.drone_fly(line_sim, screen, screen_background)



