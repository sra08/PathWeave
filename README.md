# PathWeave 🕸️ — Interactive AI Pathfinding Visualizer

An elegant, highly interactive, real-time AI pathfinding visualizer built in Python with Pygame. **PathWeave** visually demonstrates the efficiency and search space exploration patterns of classic graph-traversal algorithms.

---

## 🚀 Key Features

* **Multiple Search Algorithms:** Watch and compare:
  * **A\* Search:** Informed search algorithm using **Manhattan Distance** heuristic.
  * **Breadth-First Search (BFS):** Uninformed search guaranteeing the shortest path on unweighted graphs.
  * **Depth-First Search (DFS):** Uninformed search showing backtracking behaviors.
* **Interactive Canvas:**
  * Click & drag with Left-Click to draw obstacles/walls.
  * Right-click (or use the sidebar) to erase obstacles.
  * Set the **Start** and **End** nodes dynamically anywhere on the grid.
* **Real-time Performance Metrics:**
  * **Nodes Explored:** Track how many grid cells the algorithm searched.
  * **Path Length:** The exact number of steps from start to finish.
  * **Execution Time:** High-precision real-time execution timer.
* **Custom Simulation Speeds:** Adjust visual speed levels (Fast, Medium, Slow) to easily study step-by-step logic.
* **Modern GUI Sidebar:** Control everything effortlessly from a streamlined side panel.

---

## 🛠️ Architecture & Tech Stack

* **Language:** Python 3.8+
* **GUI / Graphics:** Pygame (hardware-accelerated rendering)
* **Design Patterns:** Iterator/Generator Pattern, Model-View-Controller (MVC) separation.

---

## 🎮 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/PathWeave.git
   cd PathWeave
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Visualizer**
   ```bash
   python main.py
   ```

---

## 📖 How it Works Under the Hood

### A* Algorithm Implementation Example
The A* implementation dynamically calculates the evaluation function $f(n) = g(n) + h(n)$, where $g(n)$ is the exact cost from the start node, and $h(n)$ is the heuristic estimation (Manhattan distance) to the goal:

$$h(n) = |x_{node} - x_{goal}| + |y_{node} - y_{goal}|$$

By using a Min-Heap queue:
```python
# From PathWeave/algorithms/astar.py
while open_heap:
    _, _, current = heapq.heappop(open_heap) # O(log N) lookup
    ...
```

---

## 🤝 Contributing

Contributions are welcome! If you'd like to implement new algorithms (like Dijkstra's or Bidirectional Search), feel free to fork the repository and submit a pull request.
