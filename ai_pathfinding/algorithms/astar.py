import heapq

class AStar:
    def __init__(self, grid):
        self.grid = grid

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a.row - b.row) + abs(a.col - b.col)

    def run(self):
        start = self.grid.start
        end = self.grid.end

        start.g = 0
        start.f = self.heuristic(start, end)
        counter = 0
        open_heap = [(start.f, counter, start)]
        open_set = {start}
        visited = set()

        while open_heap:
            _, _, current = heapq.heappop(open_heap)

            if current in visited:
                continue
            visited.add(current)
            open_set.discard(current)

            if current == end:
                self.grid.reconstruct_path()
                yield "done"
                return

            for neighbor in self.grid.neighbors(current):
                if neighbor in visited:
                    continue
                tentative_g = current.g + 1
                if tentative_g < neighbor.g:
                    neighbor.came_from = current
                    neighbor.g = tentative_g
                    neighbor.f = tentative_g + self.heuristic(neighbor, end)
                    if neighbor not in open_set:
                        counter += 1
                        heapq.heappush(open_heap, (neighbor.f, counter, neighbor))
                        open_set.add(neighbor)
                        if neighbor != end:
                            neighbor.make_frontier()

            if current != start and current != end:
                current.make_visited()
            yield current

        yield "no_path"
