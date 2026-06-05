#!/usr/bin/env python3

try:
    import random
    import time
    import subprocess
    import numpy as np
    from typing import Any, Deque
    from numpy.typing import NDArray
    from collections import deque
    import sys
except ImportError as e:
    print(e)
    exit()


class MazeGenerator():


    def __init__(self, config: dict[str, Any]) -> None:
        self.output_height = config["height"]
        self.output_width = config["width"]
        self.height = config["height"] * 2 + 1
        self.width = config["width"] * 2 + 1
        self.start = [
            (config["start"][0] - 1) * 2 + 1, (config["start"][1] - 1) * 2 + 1
        ]
        self.end = [
            (config["end"][0] - 1) * 2 + 1, (config["end"][1] - 1) * 2 + 1
        ]
        self.perfect = config["perfect"]
        self.entropy = config["entropy"]
        self.output_file = config["output_file"]
        self.seed = config["seed"]


    def fill_path(self, result: list[list[int]]) -> None:
        """Mark every cell and intermediate wall along the solution path.

        Interpolates the midpoint (door) between each consecutive cell pair in
        result, producing an interleaved sequence of cells and doors. Sets
        index [0] of each to "path" so that maze_print() can highlight them.
        Also triggers output_generator() and print_cardinal() as side effects.

        Args:
            result (list[list[int]]): Cell coordinates from end to start,
                as produced by bfs().
        """
        self.output_generator()
        self.print_cardinal(result)
        midpoints = []
        for i in range(len(result) - 1):
            temp = [int((result[i][0] + result[i + 1][0]) / 2),
                    int((result[i][1] + result[i + 1][1]) / 2)]
            midpoints.append(result[i])
            midpoints.append(temp)
        midpoints.pop(0)
        for x, y in midpoints:
            self.maze[x][y][0] = "path"

    def bfs(self) -> bool:

        if self.perfect is False:
            self.closed_walls_search()
        queue: Deque[list[int]] = deque()
        queue.append(self.start)
        visited = [self.start]
        self.maze[self.start[0]][self.start[1]][0] = 0
        cr = self.start  # cr = current position
        while queue:
            cr = queue.popleft()
            if cr == self.end:
                break
            neighbours = self.get_neighbours(cr[0], cr[1])
            for n in neighbours:
                if n not in visited:
                    self.maze[n[0]][n[1]][0] = self.maze[cr[0]][cr[1]][0] + 1
                    queue.append(n)
                    visited.append(n)
        if cr != self.end:
            return False
        way = [cr]
        while cr != self.start:
            neighbours = self.get_neighbours(cr[0], cr[1])
            for n in neighbours:
                if self.maze[n[0]][n[1]][0] == self.maze[cr[0]][cr[1]][0] - 1:
                    way.append(n)
                    if cr != self.end:
                        self.maze[cr[0]][cr[1]][0] = "path"
                    cr = n
                    break
        self.way = way
        return False

    def get_neighbours(self, x: int, y: int) -> list[list[int]]:

        directions = "eswn"
        neighbours = []
        for direction in directions:
            neighbour = self.look_forward(x, y, direction)
            if neighbour:
                neighbours.append(neighbour)
        return neighbours
