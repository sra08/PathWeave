class DFS:
    def __init__(self, grid):
        self.grid = grid

    def run(self):
        start = self.grid.start
        end = self.grid.end
        stack = [start]
        visited = set()
        start.came_from = None

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if current == end:
                self.grid.reconstruct_path()
                yield "done"
                return

            for neighbor in self.grid.neighbors(current):
                if neighbor not in visited:
                    neighbor.came_from = current
                    if neighbor != end:
                        neighbor.make_frontier()
                    stack.append(neighbor)

            if current != start and current != end:
                current.make_visited()
            yield current

        yield "no_path"
