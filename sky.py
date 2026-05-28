#!/usr/bin/env python3

from pydantic import BaseModel, ValidationError
import pygame

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

    def sky_draw_graph(self, zone_list, screen, connections):
        text = pygame.font.SysFont("Impact", 24)
        screen.fill(self.screen_color)
        for zone in zone_list:
            # print(zone.name)
            txt_pos = (zone.xy[0], zone.xy[1])
            id_text = text.render(zone.name.capitalize(), True, self.txt_color)
            pygame.draw.circle(screen, zone.color, txt_pos, zone.radius)
            screen.blit(id_text, (zone.xy[0] - 20, zone.xy[1] - 50))
        # for conn in connections:
            # print(conn)
            # for zone in zone_list:
            #     if conn.name1 == zone.name:
            #         conn.xy1 = zone.xy
            #     if conn.name2 == zone.name:
            #         conn.xy2 = zone.xy
            #     print(conn.xy1, conn.xy2)        

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

    def sky_build(self, zone_list, drone_list, connections):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((self.width, self.height))
        clock = self.clock
        dt = 0
        # print(connections)
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
            self.sky_draw_graph(zone_list, screen, connections)
            start = self.drone_fly(start, target, drone, screen, dt)
            dt = clock.tick(60) / 1000
            pygame.display.flip()
