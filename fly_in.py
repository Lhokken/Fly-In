#!/usr/bin/env python3

from typing import Any, Optional, Iterator
import pygame


class zone_factory():
    def __init__(
            self,
            name: str = "",
            start_hub: str = "",
            end_hub: str = "",
            type: str = "",
            radius: int = 20,
            max_drones: int = 1,
            priority: str = ""
            ) -> None:
        self.name: str = name
        self.xy: list[int]
        self.start_hub: str = start_hub
        self.end_hub: str = end_hub
        self.link: list[Any] = []
        self.previous: list[Any] = []
        self.type: str = type
        self.color: Any = "black"
        self.cost: int = 50000
        self.radius: int = radius
        self.max_drones: int = max_drones
        self.priority: str = priority
        self.checked: bool = False
        self.pause: bool = False


class connection_factory():
    def __init__(self) -> None:
        self.name1: str = ""
        self.name2: str = ""
        self.xy1: list[int]
        self.xy2: list[int]
        self.max_link_capacity: int = 1
        self.park: list[float]


class drone_factory():
    def __init__(
            self,
            drone_id: int,
            flyng: bool = True,
            start: Optional[pygame.Vector2] = None,
            way: Iterator[list[float]] = iter([]),
            drone_color: str = "brown",
            drone_radius: int = 15,
            place: Optional[pygame.Vector2] = None,
            direction: Optional[pygame.Vector2] = None,
            target: Optional[pygame.Vector2] = None
            ) -> None:
        self.drone_id = drone_id
        self.flyng = flyng
        self.start = start
        self.way = way
        self.drone_color = drone_color
        self.drone_radius = drone_radius
        self.place = place
        self.direction = direction
        self.target = target
        self.id_txt = pygame.font.SysFont("Arial", 12)
        self.id_rend = self.id_txt.render(
                    str(self.drone_id + 1), True, "white"
                    )

def validate_parts(parts: Any) -> bool:
    temp = parts[0].replace(" ", "")
    temp = temp.replace("-", "")
    if len(temp) != len(parts[0]):
        data_error("No \" \" or \"-\" in zones names")
        return False
    try:
        _ = int(parts[1])
        _ = int(parts[2])
    except ValueError:
        data_error("Coordinates must be integer > 0")
        return False
    return True

def validate_conn(temp: list[str], hubs: dict[Any, Any]) -> bool:
    zones = list(hubs.keys())
    if temp[0] not in zones or temp[1].split(" ")[0] not in zones:
        data_error("Connection to unknown zone")
        return False

    return True

def validate_conn_dup(connections: list[Any]) -> bool:
    for temp in connections:
        rev = temp[::-1]
        for conn in connections:
            if conn == rev:
                data_error("Error: duplicate connections")
                return False
    return True

def data_error(message: str) -> None:
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

def parse_input(input_file: str) -> dict[str, Any] | None:
    nb_drones = 0
    hubs = {}
    connections = []
    metadata = {}
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            start_hub = 0
            end_hub = 0
            dup_check = []
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("nb_drones:"):
                    try:
                        nb_drones = int(line.split(":")[1].strip())
                        if nb_drones < 1:
                            raise ValueError
                    except ValueError:
                        data_error("Drone numbers must be an integer > 0")
                        return None
                elif line.startswith(("start_hub:", "hub:", "end_hub:")):
                    if line.startswith("start_hub:"):
                        start_hub += 1
                    if line.startswith("end_hub:"):
                        end_hub += 1
                    tipo, part = line.split(":", 1)
                    cuts = part[part.find("["):part.find("]")].replace("[", "")
                    parts = part.replace(cuts, "").split()
                    if validate_parts(parts) is False:
                        return None
                    cut = cuts.split()
                    for elem in cut:
                        temp = elem.split("=")
                        metadata.update({temp[0]: temp[1]})
                    hubs.update(
                        {parts[0]: (parts[1], parts[2], tipo, metadata)}
                        )
                    dup_check.append(parts[0])
                    metadata = {}
                elif line.startswith(("connection:")):
                    tipo, partsk = line.split(":", 1)
                    conn = partsk.strip().split("-")
                    if validate_conn(conn, hubs) is False:
                        return None
                    connections.append(tuple(conn))
        print(connections)
        if len(dup_check) != len(set(dup_check)):
            data_error("No duplicate zones in the graph")
        if validate_conn_dup(connections) is False:
            return None
        if start_hub != 1 or end_hub != 1:
            data_error("Only one start_hub or end_hub")
            return None
        result = {
            "drones": nb_drones, "hubs": hubs, "connections": connections
            }
        return result
    except FileNotFoundError as e:
        print(e)
        return None
