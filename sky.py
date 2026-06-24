#!/usr/bin/env python3

from typing import Any
from collections.abc import Generator
import pygame
from fly_in import zone_factory as zone
from fly_in import drone_factory as drone
from fly_in import connection_factory as connections
import fly_in

color_set = {
    "white",
    "red",
    "green",
    "blue",
    "yellow",
    "magenta",
    "cyan"
}


def ft_color_randomizer() -> Generator[str]:
    while True:
        for color in color_set:
            yield(color)


color_randomizer = ft_color_randomizer()


class sky():
    def __init__(
            self,
            drone_list: list[drone] = [],
            line_sim: list[drone] = [],
            prox_max: int = 0,
            height: int = 900,
            widht: int = 1900,
            txt_color: str = "White",
            screen_color: tuple[int, int, int] = (0, 180, 180),
            running: str = "fly"
            ) -> None:
        pygame.init()
        pygame.font.init()
        self.graph_name: str = ""
        self.drone_list = drone_list
        self.line_sim = line_sim
        self.prox_max = prox_max
        self.height = height
        self.width = widht
        self.txt_color = txt_color
        self.screen_color = screen_color
        self.id_txt = pygame.font.SysFont("Verdana", 18)
        self.clock = pygame.time.Clock()
        self.flag = True
        self.running = running

    def sky_zone_set(self, zone_list: list[zone]) -> None:
        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0
        for zon in zone_list:
            try:
                if int(zon.xy[0]) > x_max:
                    x_max = int(zon.xy[0])
            except ValueError as e:
                print(e)
            try:
                if int(zon.xy[1]) > y_max:
                    y_max = int(zon.xy[1])
            except ValueError as e:
                print(e)
        for zon in zone_list:
            try:
                if int(zon.xy[0]) < x_min:
                    x_min = int(zon.xy[0])
            except ValueError as e:
                print(e)
            try:
                if int(zon.xy[1]) < y_min:
                    y_min = int(zon.xy[1])
            except ValueError as e:
                print(e)
        x_min = abs(x_min)
        y_min = abs(y_min)
        for zon in zone_list:
            try:
                zon.xy[0] = int(self.width / (x_max + 2 + x_min)) * \
                    (int(zon.xy[0]) + 1 + x_min)
            except ValueError as e:
                print(e)
            try:
                zon.xy[1] = int(self.height / (y_max + 2 + y_min)) * \
                    (int(zon.xy[1]) + 1 + y_min)
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
            f"{self.graph_name}      Drones: {str(dr_num)}     Priority: P "
            "    Restricted: X     Blocked: B"
            ), True, self.txt_color)
        screen.blit(id_text, (20, 20))
        for conn in connections:
            for zon in zone_list:
                if conn.name1 == zon.name:
                    conn.xy1 = zon.xy
                if conn.name2 == zon.name:
                    conn.xy2 = zon.xy
            text = pygame.font.SysFont("Impact", 22)
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
        for zon in zone_list:
            text = pygame.font.SysFont("Impact", 18)
            drn_pos = (zon.xy[0], zon.xy[1])
            random_color = next(color_randomizer)
            if zon.color == "rainbow":
                zon.color = random_color
            if zon.color == "black":
                zon.color = (70, 70, 70)
            try:
                pygame.draw.circle(screen, zon.color, drn_pos, zon.radius)
            except (TypeError, ValueError) as e:
                print(e)
            if "_" in zon.name:
                z_name = zon.name.split("_", 1)
                id_text = text.render(
                    z_name[0].capitalize(), True, self.txt_color
                    )
                screen.blit(id_text, (zon.xy[0] - 20, zon.xy[1] - 50))
                id_text = text.render(z_name[1], True, self.txt_color)
                screen.blit(id_text, (zon.xy[0] - 20, zon.xy[1] - 37))
            else:
                id_text = text.render(
                    zon.name.capitalize(), True, self.txt_color
                    )
                try:
                    screen.blit(id_text, (zon.xy[0] - 20, zon.xy[1] - 40))
                except TypeError as e:
                    print(e)
            if zon.max_drones is not None:
                id_text = text.render(str(zon.max_drones), True, "black")
                try:
                    screen.blit(id_text, (zon.xy[0] - 15, zon.xy[1] - 5))
                except TypeError as e:
                    print(e)
            if zon.priority == "priority":
                id_text = text.render("P", True, "black")
                screen.blit(id_text, (zon.xy[0] + 5, zon.xy[1] - 15))
            if zon.priority == "restricted":
                id_text = text.render("X", True, "black")
                screen.blit(id_text, (zon.xy[0] + 5, zon.xy[1] - 15))
            if zon.priority == "blocked":
                id_text = text.render("B", True, "black")
                screen.blit(id_text, (zon.xy[0] + 5, zon.xy[1] - 15))

    def drone_fly_draw(
            self,
            dron: drone,
            screen: pygame.surface.Surface,
            direction: pygame.Vector2,
            place: pygame.Vector2,
            shift
            ) -> None:
        enlarger = 0
        if direction.length() < 65 and direction.length() > 15:
            enlarger = 10
        pos = (place.x, place.y + shift)
        position = (place.x - 4, place.y - 6 + shift)
        pygame.draw.circle(
            screen,
            dron.drone_color,
            pos,
            dron.drone_radius + enlarger
            )
        screen.blit(dron.id_rend, position)

    def keyboard_input(self: "sky") -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = "quit"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            if self.running == "menu":
                self.running = "fly"
            elif self.running == "fly":
                self.running = "menu"
        if keys[pygame.K_q]:
            self.running = "quit"

    def turn_print(self, turn: list[Any], zone_list: list[zone]) -> None:
        result = []
        for id, coor in turn:
            for zon in zone_list:
                if coor == zon.xy:
                    result.append([id + 1, zon.name])
        print(result)

    def drone_park(self, goal: pygame.Vector2) -> None:
        idx = len(self.line_sim)
        temp = []
        for i in range(0, idx):
            if self.line_sim[i].start != goal:
                temp.append(self.line_sim[i])
        self.line_sim = temp

    def drone_prox_chk(self, dron: drone) -> bool:
        for elem in self.line_sim:
            if elem.start == dron.start:
                self.prox_max += 1
        if self.prox_max > 1:
            return True
        return False

    def alternative_path_search(
            self,
            dron: drone,
            zone_list: list[zone],
            connection: list[connections],
            start: zone
            ) -> bool:
        new_path = self.path_finder(zone_list, connection, start)
        if len(new_path) > dron.len_way:
            return False
        if new_path == []:
            return False
        if new_path[-1].type != "end_hub":
            return False
        idx = 0
        if start in new_path:
            idx = new_path.index(start)
        dron.way = iter(new_path[idx:])
        print("test", dron.way)
        dron.target = pygame.Vector2(next(dron.way).xy)
        return True

    def drone_fly(
            self,
            screen: pygame.surface.Surface,
            screen_background: pygame.surface.Surface,
            zone_list: list[zone],
            connections: list[connections]
            ) -> None:
        for dron in self.line_sim:
            try:
                if dron.start is not None:
                    dron.place = dron.start
            except (TypeError, IndexError):
                return
        self.drone_park(pygame.Vector2(*zone_list[-1].xy))

        while self.running == "fly":
            self.keyboard_input()
            try:
                screen.blit(screen_background, (0, 0))
                turn = []
                shift = 0

                for dron in self.line_sim:
                    if dron.target is not None and dron.place is not None and dron.flyng:
                        dron.direction = dron.target - dron.place
                        
                    self.prox_max = 0
                    if self.drone_prox_chk(dron):
                        shift = ((shift - (self.prox_max * 7)) % (self.prox_max * 30))
                    else:
                        shift = 20
                    if dron.direction is not None and dron.place is not None:
                        self.drone_fly_draw(
                            dron, screen, dron.direction, dron.place, shift - 20
                            )

                pygame.display.flip()
                for dron in self.line_sim:
                    if dron.direction is not None and dron.place is not None and dron.flyng:
                        if dron.direction.length() > 1:
                            dron.direction = dron.direction.normalize()
                            dron.place = pygame.Vector2(
                                dron.place + dron.direction * 1.1
                                )
                        elif dron.target is not None and dron.flyng:
                            turn.append(
                                [dron.drone_id,
                                    [int(dron.target[0]),
                                        int(dron.target[1])]]
                            )
                            dron.start = dron.target
            except (ValueError, UnboundLocalError) as e:
                print(e)
                exit()
            if all(dron.start == dron.target for dron in self.line_sim if dron.flyng):

                for dron in self.line_sim:
                    if dron.flyng and dron.zon_nex is not None:
                        new_target = next(dron.way, None)
                        if new_target is not None:
                            dron.target = pygame.Vector2(new_target.xy)
                        dron.zon_cur = dron.zon_nex
                        dron.zon_nex.traffic = 0
                        dron.zon_nex = new_target
                    else:    
                        dron.flyng = True

                for conn in connections:
                    conn.traffic = 0
                self.turn_print(turn, zone_list)
                break

    def zone_connections(
            self,
            zone_list: list[Any],
            connections: list[Any]
            ) -> None:
        for zon in zone_list:
            for conn in connections:
                if zon.name == conn.name1 or zon.name == conn.name2:
                    zon.link.append([conn.name1, conn.name2, conn])

    def zone_cost(self, zon: zone) -> int:
        cost: int = 0
        if zon.priority == "normal":
            cost = 1
        if zon.priority == "blocked":
            cost = 500000
        if zon.priority == "restricted":
            cost = 2
        if zon.priority == "priority":
            cost = 1
        return cost

    def path_finder(
            self,
            zone_list: list[zone],
            connections: list[connections],
            first_zone: zone
            ) -> list[zone]:
        curr_hub: list[zone] = []
        temp_hub: list[zone] = []
        path: list[zone] = []
        # normal: Standard zone with cost 1 (default)
        # blocked: Inaccessible zone. Any path using it is invalid.
        # restricted: A sensitive or dangerous zone. Costs 2.
        # priority: A preferred zone. Costs 1 turn but is prioritized.
        self.zone_connections(zone_list, connections)
        curr_hub.append(first_zone)
        curr_hub[0].checked = False
        curr_hub[0].cost = 0
        check = True
        counter = 0
        while check:
            counter += 1
            if counter > (len(zone_list) * 10):
                for zon in zone_list:
                    zon.checked = False
                for conn in connections:
                    conn.full = False
                return []
            for hub in curr_hub:
                if hub.type == "end_hub":
                    check = False
            for hub in curr_hub:
                for conn in hub.link:
                    if conn[2].full:
                        continue
                    for zon in zone_list:
                        if zon.name == conn[1] and zon.checked is False:
                            if zon.priority == "blocked":
                                continue
                            elif zon.priority == "priority":
                                zon.previous = conn[0]
                                zon.checked = True
                                temp_hub.append(zon)
                            elif zon.priority == "restricted":
                                if zon.pause is True:
                                    zon.previous = conn[0]
                                    zon.checked = True
                                    zon.pause = False
                                    temp_hub.append(zon)
                                    # print("temp_hub.append", zon)
                                elif zon.pause is False:
                                    zon.pause = True
                                    temp_hub.append(hub)
                                    # print("temp_hub.append", hub)
                            else:
                                zon.previous = conn[0]
                                zon.cost = 1 + hub.cost
                                zon.checked = True
                                temp_hub.append(zon)
            curr_hub = []
            curr_hub = temp_hub
            temp_hub = []
        zone_dict = {}
        zone_dict = {
            zone.name: zone for zone in zone_list if (
                not zone.previous == [] and zone is not None
                )
                }
        curr = zone_list[-1]
        path.append(curr)
        for zon in zone_list:
            zon.checked = False
        while True:
            next = zone_dict.get(str(curr.previous))
            if next is None:
                path.append(zone_list[0])
                break
            path.append(next)
            curr = next
        for conn in connections:
            conn.full = False
        return path[::-1]

    def traffic_ruler(
            self,
            start: zone,
            target: zone,
            connection: list[connections]
            ) -> int:
        curr_conn = (fly_in.get_connection(
            start.name, target.name, connection)
            )
        if target.max_drones is not None:
            if int(target.max_drones) < curr_conn.max_link_capacity:
                return int(target.max_drones)
        if curr_conn is not None:
            return curr_conn.max_link_capacity
        return 5000

    def sky_build(
            self,
            zone_list: list[zone],
            drone_list: list[drone],
            connections: list[connections]
            ) -> None:
        pygame.init()
        pygame.font.init()
        if connections == [] or zone_list == []:
            return
        screen = pygame.display.set_mode((self.width, self.height))
        self.sky_zone_set(zone_list)
        screen_background = pygame.Surface((self.width, self.height))
        self.sky_draw_graph(
            zone_list, screen_background, connections, len(drone_list)
            )
        hub_list = self.path_finder(zone_list, connections, zone_list[0])

        self.drone_list = drone_list
        iter_drone = iter(self.drone_list)
        self.flag = True
        self.line_sim = []
        while self.running == "fly":
            self.keyboard_input()
            if self.flag is True:
                for _ in range(0, self.traffic_ruler(hub_list[0], hub_list[1], connections)):
                    tdron = next(iter_drone, None)
                    hub_list = self.path_finder(zone_list, connections, zone_list[0])
                    if tdron is not None:
                        tdron.start = pygame.Vector2(*(hub_list[0].xy))
                        tdron.target = pygame.Vector2(*(hub_list[1].xy))
                        tdron.zon_cur = hub_list[0]
                        tdron.zon_nex = hub_list[1]
                        tdron.len_way = len(hub_list)
                        tdron.way = iter(hub_list[2:])
                        self.line_sim.append(tdron)
                    elif self.line_sim == []:
                        self.flag = False
                    continue

                for dron in self.line_sim:
                    if dron.zon_nex is not None and dron.zon_cur is not None:
                        curr_conn = (fly_in.get_connection(
                            dron.zon_cur.name, dron.zon_nex.name, connections)
                            )
                        curr_conn.traffic += 1
                        if curr_conn.traffic > curr_conn.max_link_capacity:
                            dron.zon_cur.traffic += 1
                            # dron.flyng = False
                            curr_conn.full = True
                            if not self.alternative_path_search(
                                dron, zone_list, connections, dron.zon_cur):
                                dron.flyng = False
                            curr_conn.full = False
                            

                for dron in self.line_sim:
                    if dron.zon_nex is not None:
                        if dron.zon_nex.max_drones is not None:
                            if dron.zon_nex.traffic >= int(dron.zon_nex.max_drones):
                                dron.flyng = False
                            else:
                                dron.zon_nex.traffic += 1
    
                self.drone_fly(screen, screen_background, zone_list, connections)
