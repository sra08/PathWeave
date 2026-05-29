import pygame
import sys
from grid import Grid
from visualizer import Visualizer
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.astar import AStar

# ── Window Config ──────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 900, 700
SIDEBAR_W = 220
GRID_W = WIDTH - SIDEBAR_W
ROWS, COLS = 30, 30
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🤖 AI Pathfinding Simulator")
clock = pygame.time.Clock()

grid = Grid(ROWS, COLS, GRID_W, HEIGHT)
viz = Visualizer(screen, grid, GRID_W, SIDEBAR_W, WIDTH, HEIGHT)

# State
algorithm_names = ["A*", "BFS", "DFS"]
algo_index = 0
speed_levels = [0.005, 0.02, 0.08]   # seconds per step (fast→slow)
speed_names = ["Fast", "Medium", "Slow"]
speed_index = 1

running_algo = False
algo_gen = None
path_found = False
no_path = False
stats = {"nodes": 0, "path_len": 0, "time": 0.0}
mode = "draw"   # "draw" or "erase"
placing = None  # "start" or "end"

import time

def get_algo():
    name = algorithm_names[algo_index]
    if name == "BFS":
        return BFS(grid)
    elif name == "DFS":
        return DFS(grid)
    else:
        return AStar(grid)

def reset_search():
    global running_algo, algo_gen, path_found, no_path, stats
    running_algo = False
    algo_gen = None
    path_found = False
    no_path = False
    stats = {"nodes": 0, "path_len": 0, "time": 0.0}
    grid.clear_visited()

start_time = None

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ── Button clicks ──────────────────────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Sidebar buttons
            btn = viz.get_button_at(mx, my)
            if btn == "run":
                if grid.start and grid.end and not running_algo:
                    reset_search()
                    algo = get_algo()
                    start_time = time.time()
                    algo_gen = algo.run()
                    running_algo = True
            elif btn == "reset":
                grid.clear_all()
                reset_search()
            elif btn == "clear_path":
                reset_search()
            elif btn == "algo_left":
                algo_index = (algo_index - 1) % len(algorithm_names)
                reset_search()
            elif btn == "algo_right":
                algo_index = (algo_index + 1) % len(algorithm_names)
                reset_search()
            elif btn == "speed_left":
                speed_index = (speed_index - 1) % len(speed_levels)
            elif btn == "speed_right":
                speed_index = (speed_index + 1) % len(speed_levels)
            elif btn == "set_start":
                placing = "start"
            elif btn == "set_end":
                placing = "end"
            elif btn == "draw":
                placing = None
                mode = "draw"
            elif btn == "erase":
                placing = None
                mode = "erase"

            # Grid click
            elif mx < GRID_W:
                cell = grid.get_cell(mx, my)
                if cell:
                    if placing == "start":
                        grid.set_start(cell)
                        placing = None
                    elif placing == "end":
                        grid.set_end(cell)
                        placing = None
                    elif mode == "draw":
                        if cell != grid.start and cell != grid.end:
                            cell.make_wall()
                    elif mode == "erase":
                        if cell != grid.start and cell != grid.end:
                            cell.reset()

        # Drag to draw/erase walls
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if mx < GRID_W and not placing:
                cell = grid.get_cell(mx, my)
                if cell and cell != grid.start and cell != grid.end:
                    if mode == "draw":
                        cell.make_wall()
                    elif mode == "erase":
                        cell.reset()

        if pygame.mouse.get_pressed()[2]:
            mx, my = pygame.mouse.get_pos()
            if mx < GRID_W:
                cell = grid.get_cell(mx, my)
                if cell and cell != grid.start and cell != grid.end:
                    cell.reset()

    # ── Algorithm step ─────────────────────────────────────────────────────────
    if running_algo and algo_gen:
        try:
            result = next(algo_gen)
            stats["nodes"] += 1
            if result == "done":
                elapsed = time.time() - start_time
                stats["time"] = round(elapsed, 3)
                path_found = True
                running_algo = False
                # count path length
                c = grid.end
                length = 0
                while c and c.came_from:
                    c = c.came_from
                    length += 1
                stats["path_len"] = length
            elif result == "no_path":
                elapsed = time.time() - start_time
                stats["time"] = round(elapsed, 3)
                no_path = True
                running_algo = False
            pygame.time.delay(int(speed_levels[speed_index] * 1000))
        except StopIteration:
            running_algo = False

    viz.draw(
        algo_name=algorithm_names[algo_index],
        speed_name=speed_names[speed_index],
        running=running_algo,
        path_found=path_found,
        no_path=no_path,
        stats=stats,
        mode=mode,
        placing=placing
    )
    pygame.display.flip()
