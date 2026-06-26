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
    """Simple color random generator, used only by
    impossible_goal because it has color = rainbow
    """
    while True:
        for color in color_set:
            yield(color)


color_randomizer = ft_color_randomizer()


class sky():
    """This is the class that represent the map, sky, whatever
    you think is best where drones move along connections between
    zones, from start to end.
    """
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
        self.turn: int = 1
        self.id_incr: int = 0

    def sky_zone_set(self, zone_list: list[zone]) -> None:
        """This analize zone coordinates for each zone in
        zone list, find max and min then calculate new coordinates
        in pixel in order to place each zon in the correct place in
        the windows. This method respect windows dimension in pixels
        """
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
        """This method use pygame to draw the real graph on the given window,
        place zones and connection with relevant data near. Max link
        connections is printed in the midle of the line.
        """
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
            direction: pygame.math.Vector2,
            place: pygame.math.Vector2,
            shift: int
            ) -> None:
        """Draw the circle of the drone, it's id and the right color
        on the screen surface, but it do not appera on the monitor
        at this time.
        but """
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
        """Th only purpose is to get keyboard input and assign in
        the right place.
        """
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
        """The only purpose is to print in the terminal
        each line turn
        """
        result = []
        for id, coor in turn:
            for zon in zone_list:
                if coor == zon.xy:
                    result.append([id + 1, zon.name])
        if result != []:
            print(f"{self.turn}: {result}")
        self.turn += 1

    def drone_park(self, goal: pygame.math.Vector2) -> None:
        """This method simpy get the drone out of the screen
        when it arrive on the goal zone
        """
        idx = len(self.line_sim)
        temp = []
        for i in range(0, idx):
            if self.line_sim[i].start != goal:
                temp.append(self.line_sim[i])
        self.line_sim = temp

    def drone_prox_chk(self, dron: drone) -> bool:
        """This method calculate how many drone occupy
        th same point on the screen, in order to move them
        a little and make clear how many they are
        """
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
        """This method is called when a drone find a restriction in
        a connection, and change the drone path if a new one not
        longer has been found. Otherwise it return False.
        """

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

        dron.way = iter(tuple(new_path[idx + 1:]))
        dron.zon_nex = next(dron.way)

        dron.target = pygame.math.Vector2(
            float(dron.zon_nex.xy[0]), float(dron.zon_nex.xy[1])
            )
        return True

    def next_turn(self) -> None:
        """This method change parameters for the next turn, giving
        drones the next target and next start.
        It also set to zero zone traffic parameter
        """
        for dron in self.line_sim:
            if dron.flyng and dron.zon_nex is not None:
                new_target = next(dron.way, None)
                if new_target is not None:
                    dron.target = pygame.math.Vector2(
                        float(new_target.xy[0]),
                        float(new_target.xy[1])
                        )
                dron.zon_cur = dron.zon_nex
                dron.zon_nex.traffic = 0
                dron.zon_nex = new_target
            else:
                dron.flyng = True

    def drone_fly(
            self,
            screen: pygame.surface.Surface,
            screen_background: pygame.surface.Surface,
            zone_list: list[zone],
            connections: list[connections]
            ) -> None:
        """This is a very long method, it read the list of flying
        drones and make them graphically move from a zone to the next.
        """
        for dron in self.line_sim:
            try:
                if dron.start is not None:
                    dron.place = dron.start
            except (TypeError, IndexError):
                return
        self.drone_park(pygame.math.Vector2(
            *(next(zon for zon in zone_list if zon.type == "end_hub")).xy))
        while self.running == "fly":
            self.keyboard_input()
            try:
                screen.blit(screen_background, (0, 0))
                turn = []
                shift = 0
                for dron in self.line_sim:
                    if dron.target is not None\
                            and dron.place is not None and dron.flyng:
                        dron.direction = dron.target - dron.place
                    self.prox_max = 0
                    if self.drone_prox_chk(dron):
                        shift = (
                            (shift - (self.prox_max * 7))
                            % (self.prox_max * 30)
                            )
                    else:
                        shift = 20
                    if dron.direction is not None and dron.place is not None:
                        self.drone_fly_draw(
                            dron,
                            screen,
                            dron.direction,
                            dron.place,
                            shift - 20
                            )
                pygame.display.flip()
                for dron in self.line_sim:
                    if dron.direction is not None\
                            and dron.place is not None and dron.flyng:
                        if dron.direction.length() > 1:
                            dron.direction = dron.direction.normalize()
                            dron.place = pygame.math.Vector2(
                                dron.place + dron.direction * 1.7
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
            if all(dron.start == dron.target for dron
                    in self.line_sim if dron.flyng):
                self.next_turn()
                for conn in connections:
                    conn.traffic = 0
                self.turn_print(turn, zone_list)
                break

    def zone_connections(
            self,
            zone_list: list[zone],
            connection: list[connections]
            ) -> None:
        for zon in zone_list:
            if zon.priority == "restricted":
                zone_list.append(self.new_zone())
                for conn in connection:
                    if conn.name2 == zon.name:
                        conn.name2 = zone_list[-1].name
                new_conn = connections()
                new_conn.name2 = zon.name
                new_conn.name1 = zone_list[-1].name
                connection.append(new_conn)

        for zon in zone_list:
            for conn in connection:
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
                                elif zon.pause is False:
                                    zon.pause = True
                                    temp_hub.append(hub)
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
        curr = next(zon for zon in zone_list if zon.type == "end_hub")
        path.append(curr)
        for zon in zone_list:
            zon.checked = False
        counter = 0
        while True:
            counter += 1
            if counter > (len(zone_list) * 10):
                break
            nex = zone_dict.get(str(curr.previous))

            if nex is None:
                path.append(zone_list[0])
                break
            path.append(nex)
            curr = nex
        # for elem in path:
        #     print("path", elem.name)
        for conn in connections:
            conn.full = False
        return path[::-1]

    def new_zone(self) -> zone:
        self.id_incr += 1
        new_zone = zone()
        new_zone.name = f"virtual_zon{self.id_incr}"
        new_zone.type = "virtual"
        new_zone.color = "white"
        new_zone.max_drones = 50
        new_zone.priority = "normal"
        new_zone.radius = 9
        new_zone.traffic = 0
        new_zone.xy = [0, 0]
        return new_zone

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

    def drone_inizialize(
            self,
            tdron: drone | None,
            hub_list: list[zone]
            ) -> None:
        """This method set starting parameters to drones just
        leaving start zone. Then it append the new drone/drones
        to self.line_sim
        """
        if tdron is not None:
            tdron.start = pygame.math.Vector2(*(hub_list[0].xy))
            tdron.target = pygame.math.Vector2(*(hub_list[1].xy))
            tdron.zon_cur = hub_list[0]
            tdron.zon_nex = hub_list[1]
            tdron.len_way = len(hub_list)
            tdron.way = iter(hub_list[2:])
            self.line_sim.append(tdron)
        elif self.line_sim == []:
            self.flag = False

    def sky_build(
            self,
            zone_list: list[zone],
            drone_list: list[drone],
            connections: list[connections]
            ) -> None:
        """This inizialize some parameters, such as screen and background.
        It also let multiple drone leave togheter if it's possible,
        and launch alternative path if a drone find a restricted way.
        Last this method let a drone wait if there is no space left to move on.
        """
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
        self.zone_connections(zone_list, connections)
        hub_list = self.path_finder(zone_list, connections, zone_list[0])

        for i in range(1, len(hub_list)):
            if hub_list[i].type == "virtual":
                hub_list[i].xy[0] = (
                    hub_list[i - 1].xy[0] + hub_list[i + 1].xy[0]) // 2
                hub_list[i].xy[1] = (
                    hub_list[i - 1].xy[1] + hub_list[i + 1].xy[1]) // 2
                print(
                    "<coor>", hub_list[i - 1].xy,
                    hub_list[i].xy, hub_list[i + 1].xy
                    )
        self.drone_list = drone_list
        iter_drone = iter(self.drone_list)
        self.flag = True
        self.line_sim = []
        self.turn = 1
        while self.running == "fly":
            self.keyboard_input()
            if self.flag is True:
                for _ in range(0, self.traffic_ruler(
                        hub_list[0], hub_list[1], connections)):
                    tdron = next(iter_drone, None)
                    hub_list = self.path_finder(
                        zone_list, connections, zone_list[0])
                    self.drone_inizialize(tdron, hub_list)

                for dron in self.line_sim:
                    if dron.zon_nex is not None and dron.zon_cur is not None:
                        curr_conn = (fly_in.get_connection(
                            dron.zon_cur.name, dron.zon_nex.name, connections)
                            )
                        curr_conn.traffic += 1
                        if curr_conn.traffic > curr_conn.max_link_capacity:
                            dron.zon_cur.traffic += 1
                            curr_conn.full = True
                            if dron.zon_cur.name != "virtual_zon":
                                if self.alternative_path_search(
                                        dron, zone_list,
                                        connections,
                                        dron.zon_cur
                                        ):
                                    dron.zon_cur.traffic -= 1
                                else:
                                    dron.flyng = False
                for dron in self.line_sim:
                    if dron.zon_nex is not None:
                        if dron.zon_nex.max_drones is not None:
                            if dron.zon_nex.traffic >= int(
                                    dron.zon_nex.max_drones):
                                dron.flyng = False
                            else:
                                dron.zon_nex.traffic += 1
                self.drone_fly(
                    screen, screen_background, zone_list, connections)
