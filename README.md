*This project was developed by **gcerrete** as part of the 42 curriculum.*

# Fly-In

This project manages a fleet of drones navigating through paths within a given graph structure. While there are multiple possible routes, a Breadth-First Search (BFS) algorithm is utilized to determine the most efficient path to reach the target destination. Furthermore, this calculated route can be dynamically modified in real-time while the drones are in transit, allowing for highly adaptable pathfinding.

## Description

The application's execution begins by scanning and analyzing a specified directory containing map files. The parser iteratively searches through all identified folders and thoroughly examines each file within them. Based on the volume of discovered directories and files, a dynamic and scalable menu is generated. Users can navigate this interface and make their selections using keyboard inputs, with the active keybindings clearly displayed at the top of the screen for an intuitive user experience.

## Instructions

Use the following `make` commands in your terminal to set up, run, and manage the project:

* **`make install`**: Initializes and installs project dependencies using `uv sync`.
* **`make run`**: Executes the main program by launching `uv run a_maze_ing.py config.txt`.
* **`make debug`**: Starts the Python Debugger (`pdb`) tool for troubleshooting and code inspection.
* **`make clean`**: Removes the `uv` installation files and cleans up the working environment.
* **`make lint`**: Runs standard static code analysis and quality checks using `flake8` and `mypy`.
* **`make lint-strict`**: Runs rigorous code quality checks by executing `flake8` and `mypy` with the `--strict` flag enabled.

## Resources

* The official [Pygame documentation](https://www.pygame.org/news) was a vital resource for understanding and implementing the graphical and interactive components of this project.
* Gemini AI was utilized as a theoretical learning aid. To ensure a solid understanding of the underlying logic, the AI was strictly instructed to provide conceptual guidance and explanations rather than outputting ready-to-use code, unless explicitly requested.