#!/usr/bin/env python3

from pydantic import ValidationError
from typing import Any
import pygame
from sky import sky
from fly_in import zone_factory
from fly_in import connection_factory
from fly_in import drone_factory
from fly_in import parse_input
from fly_menu import menu



def zone_build(input_list: dict[str, list[Any]]) -> list[Any]:
    zone_list = []
    for key, value in input_list.items():
        zone = zone_factory()
        zone.name = key
        zone.xy = [value[0], value[1]]
        zone.type = value[2]
        zone.color = value[3].get("color")
        zone.max_drones = value[3].get("max_drones")
        zone.priority = value[3].get("zone")
        zone_list.append(zone)
    return zone_list


def drone_build(drone_number: int) -> list[Any]:
    drone_list = []
    for i in range(0, drone_number):
        drone = drone_factory(i, [80, 80])
        drone.drone_id = i
        drone_list.append(drone)
    return drone_list


def connection_build(connections: list[Any]) -> list[Any]:
    connect_list = []
    for elem in connections:
        connection = connection_factory()
        connection.name1 = elem[0]
        if "[" in elem[1]:
            parse = elem[1].split()
            connection.name2 = parse[0]
            connection.max_link_capacity = (parse[1].split("=")[1]).strip("]")
        else:
            connection.name2 = elem[1]
        connect_list.append(connection)
    return connect_list


def main() -> None:

    sky_menu = menu("maps")
    sky_menu.menu_sky()
    running = True

    skypath = sky()

    sky_menu.menu_zone_set(skypath.width, skypath.height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            break
        sky_menu.menu_build(skypath.width, skypath.height)

        sky_1 = parse_input("maps/hard/03_ultimate_challenge.txt")

        hubs = sky_1["hubs"]
        drones = sky_1["drones"]
        connections = sky_1["connections"]

        zones = zone_build(hubs)
        drone_list = drone_build(drones)
        connect_list = connection_build(connections)

        skypath.sky_build(zones, drone_list, connect_list)

    pygame.quit()


if __name__ == "__main__":
    main()
