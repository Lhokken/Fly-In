#!/usr/bin/env python3

from pydantic import BaseModel, ValidationError
import pygame
from sky import sky
from fly_in import zone_factory
from fly_in import connection_factory
from fly_in import drone_factory
from fly_in import parse_input


def zone_build(input_list) -> list:
    zone_list = []
    for key, value in input_list.items():
        zone = zone_factory()
        max_drones = 1
        if len(value) == 5:
            max_drones = value[4][11:-1]
        zone.name = key
        zone.xy = [value[0], value[1]]
        zone.type = value[2]
        zone.color = value[3][7:]
        zone.max_drones = max_drones
        zone_list.append(zone)
    return zone_list


def drone_build(drone_number):
    drone_list = []
    for i in range(0, drone_number):
        drone = drone_factory(i, [80, 80])
        drone.drone_id = i
        drone_list.append(drone)
    return drone_list


def connection_build(connections):
    connect_list = []
    for elem in connections:
        connection = connection_factory()
        connection.name1 = elem[0]
        print(elem)
        if "[" in elem[1]:
            parse = elem[1].split()
            print("<>", parse)
            connection.name2 = parse[0]
            connection.max_link_capacity = (parse[1].split("=")[1]).strip("]")
        else:
            connection.name2 = elem[1]
        print("name1", connection.name1)
        print("name2", connection.name2)
        print("max", connection.max_link_capacity)
        connect_list.append(connection)
    return connect_list



def main():
    skypath = sky()
    sky_1 = parse_input("maps/medium/01_dead_end_trap.txt")
    drone_list = drone_build(sky_1["drones"])

    hubs = sky_1["hubs"]
    zones = zone_build(hubs)
    connections = sky_1["connections"]
    connect_list = connection_build(connections)

    skypath.sky_build(zones, drone_list, connections)

    pygame.quit()


if __name__ == "__main__":
    main()
