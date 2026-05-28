#!/usr/bin/env python3

from pydantic import BaseModel, ValidationError
import pygame
# from sky import sky


class zone_factory():
    def __init__(
            self,
            name: str="",
            start_hub: str="",
            end_hub: str="",
            type: str="",
            radius: int=30,
            max_drones: int=1,
            next: list=[tuple],
            ) -> None:
        self.name = name
        self.xy: list=[0, 0]
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.type = type
        self.color = "black"
        self.radius = radius
        self.max_drones = max_drones
        self.next = next


class connection_factory():
    def __init__(self) -> None:
        self.name1 = ""
        self.name2 = ""
        self.xy1 = ()
        self.xy2 = ()
        self.max_link_capacity = 1

    # def connection_build(self, connections):
    #     for conn in connections:




class drone_factory():
    def __init__(
            self,
            drone_id,
            start,
            drone_color="brown",
            drone_radius=20
            ) -> None:
        self.drone_id = drone_id
        self.start = start
        self.drone_color = drone_color
        self.drone_radius = drone_radius
        self.id_txt = pygame.font.SysFont("Arial", 24)
        self.id_rend = self.id_txt.render(
                    str(self.drone_id), True, "white"
                    )



def drone_build(drone_number):
    drone_list = []
    for i in range(0, drone_number):
        drone = drone_factory(i, [80, 80])
        drone.drone_id = i
        drone_list.append(drone)
    return drone_list


def parse_input(input_file: str):
    nb_drones = 0
    hubs = {}
    connections = []
    tipo = ""
    parts = ""
    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("nb_drones:"):
                nb_drones = int(line.split(":")[1].strip())
            elif line.startswith(("start_hub:", "hub:", "end_hub:")):
                tipo, resto = line.split(":", 1)
                parts = resto.strip().split()
                parts[3] = parts[3].replace("]", "")
                if len(parts) == 5:
                    hubs.update({parts[0]: (parts[1], parts[2], tipo, parts[3], parts[4])})
                else:
                    hubs.update({parts[0]: (parts[1], parts[2], tipo, parts[3])})
            elif line.startswith(("connection:")):
                tipo, resto = line.split(":", 1)
                parts = resto.strip().split("-")
                connections.append(tuple(parts))
    return {"drones": nb_drones, "hubs": hubs, "connections": connections}
