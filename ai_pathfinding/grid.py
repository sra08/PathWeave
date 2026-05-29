import pygame

# Colors
WHITE       = (255, 255, 255)
BLACK       = (20,  20,  30)
WALL        = (30,  30,  50)
START       = (39,  174, 96)
END         = (231, 76,  60)
VISITED     = (52,  152, 219)
FRONTIER    = (133, 193, 233)
PATH        = (241, 196, 15)
GRID_LINE   = (200, 210, 220)


class Cell:
    def __init__(self, row, col, cell_w, cell_h):
        self.row = row
        self.col = col
        self.cell_w = cell_w
        self.cell_h = cell_h
        self.x = col * cell_w
        self.y = row * cell_h
        self.state = "empty"   # empty|wall|start|end|visited|frontier|path
        self.came_from = None
        self.g = float("inf")
        self.f = float("inf")

    def is_wall(self): return self.state == "wall"
    def make_wall(self): self.state = "wall"
    def make_visited(self): self.state = "visited"
    def make_frontier(self): self.state = "frontier"
    def make_path(self): self.state = "path"

    def reset(self):
        self.state = "empty"
        self.came_from = None
        self.g = float("inf")
        self.f = float("inf")

    def reset_search(self):
        if self.state in ("visited", "frontier", "path"):
            self.state = "empty"
        self.came_from = None
        self.g = float("inf")
        self.f = float("inf")

    def color(self):
        return {
            "empty":    WHITE,
            "wall":     WALL,
            "start":    START,
            "end":      END,
            "visited":  VISITED,
            "frontier": FRONTIER,
            "path":     PATH,
        }.get(self.state, WHITE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color(),
                         (self.x + 1, self.y + 1, self.cell_w - 1, self.cell_h - 1))

    def __lt__(self, other):
        return self.f < other.f

    def __repr__(self):
        return f"Cell({self.row},{self.col})"


class Grid:
    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.cell_w = width // cols
        self.cell_h = height // rows
        self.cells = [[Cell(r, c, self.cell_w, self.cell_h)
                       for c in range(cols)] for r in range(rows)]
        self.start = None
        self.end = None

    def get_cell(self, mx, my):
        col = mx // self.cell_w
        row = my // self.cell_h
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.cells[row][col]
        return None

    def neighbors(self, cell):
        result = []
        r, c = cell.row, cell.col
        dirs = [(-1,0),(1,0),(0,-1),(0,1)]
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                n = self.cells[nr][nc]
                if not n.is_wall():
                    result.append(n)
        return result

    def set_start(self, cell):
        if self.start:
            self.start.reset()
        self.start = cell
        cell.state = "start"

    def set_end(self, cell):
        if self.end:
            self.end.reset()
        self.end = cell
        cell.state = "end"

    def clear_all(self):
        for row in self.cells:
            for cell in row:
                cell.state = "empty"
                cell.came_from = None
                cell.g = float("inf")
                cell.f = float("inf")
        self.start = None
        self.end = None

    def clear_visited(self):
        for row in self.cells:
            for cell in row:
                cell.reset_search()
        if self.start:
            self.start.state = "start"
        if self.end:
            self.end.state = "end"

    def draw(self, screen):
        screen.fill((220, 230, 240))
        for row in self.cells:
            for cell in row:
                cell.draw(screen)
        # Grid lines
        for c in range(self.cols + 1):
            pygame.draw.line(screen, GRID_LINE,
                             (c * self.cell_w, 0), (c * self.cell_w, self.height), 1)
        for r in range(self.rows + 1):
            pygame.draw.line(screen, GRID_LINE,
                             (0, r * self.cell_h), (self.width, r * self.cell_h), 1)

    def reconstruct_path(self):
        cell = self.end
        while cell and cell.came_from:
            cell.make_path()
            cell = cell.came_from
        if self.start:
            self.start.state = "start"
        if self.end:
            self.end.state = "end"
