#!/usr/bin/env python3

from pydantic import BaseModel, ValidationError
import pygame
from ft_coordinate_system import ft_coordinate_system

class sky():
    def __init__(
            self,
            height=900,
            widht=1900,
            txt_color="White",
            screen_color="Orange",
            ) -> None:
        pygame.init()
        pygame.font.init()
        self.height = height
        self.width = widht
        self.txt_color = txt_color
        self.screen_color = screen_color
        self.id_txt = pygame.font.SysFont("Impact", 18)
        self.clock = pygame.time.Clock()

    def sky_zone_set(self, zone_list):
        x_max = 0
        y_max = 0
        for zone in zone_list:
            if int(zone.xy[0]) > x_max:
                x_max = int(zone.xy[0])
            if int(zone.xy[1]) > y_max:
                y_max = int(zone.xy[1])
        for zone in zone_list:
            zone.xy[0] = int(self.width / (x_max + 2)) * (int(zone.xy[0]) + 1)
            zone.xy[1] = int(self.height / (y_max + 2)) * (int(zone.xy[1]) + 1)

    def sky_draw_graph(self, zone_list, screen):
        text = pygame.font.SysFont("Impact", 24)
        screen.fill(self.screen_color)
        for zone in zone_list:
            txt_pos = (zone.xy[0], zone.xy[1])
            id_text = text.render(zone.name.capitalize(), True, self.txt_color)
            pygame.draw.circle(screen, zone.color, txt_pos, zone.radius)
            screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 50))
            

    def drone_fly(self, a: list, b: list, drone, screen, dt):
        start = pygame.Vector2(a[0], a[1])
        target = pygame.Vector2(b[0], b[0])
        direction = target - start
        txt_pos = (start.x - 7, start.y - 12)
        pygame.draw.circle(screen, drone.drone_color, start, drone.drone_radius)
        screen.blit(drone.id_rend, txt_pos)
        direction = target - start
        if direction.length() > 5:
            direction = direction.normalize()
            start += direction * 300 * dt
        pygame.display.flip()
        return [int(start[0]), int(start[1])]

    def sky_build(self, zone_list):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = self.clock
        dt = 0
        running = True
        start = [50, 50]
        target = [400, 1700]
        self.sky_zone_set(zone_list)
        drone = drone_list[0]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                break       
            self.sky_draw_graph(zone_list, screen)
            start = self.drone_fly(start, target, drone, screen, dt)
            dt = clock.tick(60) / 1000
            pygame.display.flip()


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

    def zone_build(self, input_list) -> list:
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


class connection_factory():
    def __init__(self, name1, name2, max_link_capacity=1) -> None:
        self.name1 = name1
        self.name2 = name2
        self.max_link_capacity = max_link_capacity
        
        pass


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



if __name__ == "__main__":
    skypath = sky()
    zones = zone_factory()

    sky_1 = parse_input("maps/medium/01_dead_end_trap.txt")
    drone_list = drone_build(sky_1["drones"])
    hubs = sky_1["hubs"]
    connections = sky_1["connections"]
    
    zones = zones.zone_build(hubs)

    skypath.sky_build(zones)

    pygame.quit()
