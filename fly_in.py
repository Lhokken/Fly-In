#!/usr/bin/env python3

from typing import Any
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
        self.link: list = []
        self.previous: list[Any] = []
        self.type: str = type
        self.color: Any = "black"
        self.cost: int = 50000
        self.radius: int = radius
        self.max_drones: int = max_drones
        self.priority: str = priority
        self.checked: bool = False


class connection_factory():
    def __init__(self) -> None:
        self.name1: str = ""
        self.name2: str = ""
        self.xy1: list[int]
        self.xy2: list[int]
        self.max_link_capacity: int = 1


class drone_factory():
    def __init__(
            self,
            drone_id: int,
            start: list[int],
            drone_color: str = "brown",
            drone_radius: int = 15
            ) -> None:
        self.drone_id = drone_id
        self.start = start
        self.drone_color = drone_color
        self.drone_radius = drone_radius
        self.id_txt = pygame.font.SysFont("Arial", 12)
        self.id_rend = self.id_txt.render(
                    str(self.drone_id + 1), True, "white"
                    )


def parse_input(input_file: str) -> dict[str, Any] | None:
    nb_drones = 0
    hubs = {}
    connections = []
    metadata = {}
    try:
        with open(input_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.startswith("nb_drones:"):
                    nb_drones = int(line.split(":")[1].strip())
                elif line.startswith(("start_hub:", "hub:", "end_hub:")):
                    tipo, part = line.split(":", 1)
                    cuts = part[part.find("["):part.find("]")].replace("[", "")
                    parts = part.replace(cuts, "").split()
                    cut = cuts.split()
                    for elem in cut:
                        temp = elem.split("=")
                        metadata.update({temp[0]: temp[1]})
                    hubs.update(
                        {parts[0]: (parts[1], parts[2], tipo, metadata)}
                        )
                    metadata = {}
                elif line.startswith(("connection:")):
                    tipo, partsk = line.split(":", 1)
                    temp = partsk.strip().split("-")
                    connections.append(tuple(temp))
        result = {
            "drones": nb_drones, "hubs": hubs, "connections": connections
            }
        return result
    except FileNotFoundError as e:
        print(e)
        return None
