#!/usr/bin/env python3

import pygame
import sys
from typing import Any
from sky import sky
from fly_in import zone_factory
from fly_in import connection_factory
from fly_in import drone_factory
from fly_in import parse_input, data_error
from fly_menu import menu


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


def zone_build(input_list: dict[str, list[Any]]) -> list[zone_factory]:
    zone_list = []
    for key, value in input_list.items():
        zone = zone_factory()
        zone.name = key
        zone.xy = [value[0], value[1]]
        zone.type = value[2]
        zone.color = value[3].get("color")
        zone.max_drones = value[3].get("max_drones")
        zone.priority = value[3].get("zone", "normal")
        zone_list.append(zone)
    return zone_list


def drone_build(drone_number: int) -> list[Any]:
    drone_list = []
    for i in range(0, drone_number):
        drone = drone_factory(i)
        drone.drone_id = i
        drone_list.append(drone)
    return drone_list


def main() -> None:

    sky_menu = menu("maps")
    sky_menu.menu_file_mapping()
    skypath = sky()
    sky_menu.menu_zone_set(skypath.width, skypath.height)
    while not skypath.running == "quit":
        skypath.keyboard_input()
        sky_menu.menu_builder(skypath.width, skypath.height)
        sky_1 = parse_input(sky_menu.file_path)
        if sky_1 is None:
            continue
        elif skypath.running == "fly":
            skypath.sky_build(
                zone_build(sky_1["hubs"]),
                drone_build(sky_1["drones"]),
                connection_build(connections=sky_1["connections"])
                )
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
