from collections import deque

class BFS:
    def __init__(self, grid):
        self.grid = grid

    def run(self):
        start = self.grid.start
        end = self.grid.end
        queue = deque([start])
        visited = {start}
        start.came_from = None

        while queue:
            current = queue.popleft()
            if current == end:
                self.grid.reconstruct_path()
                yield "done"
                return
            for neighbor in self.grid.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    neighbor.came_from = current
                    if neighbor != end:
                        neighbor.make_frontier()
                    queue.append(neighbor)
            if current != start and current != end:
                current.make_visited()
            yield current

        yield "no_path"
