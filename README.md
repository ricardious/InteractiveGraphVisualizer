### Project Overview

This project is an interactive graph visualizer built using **PyQt5** for the user interface, **NetworkX** for graph data structure and algorithms, and **PyVis** for web-based graph visualization. It allows users to create and interact with graphs by adding vertices and edges, and applying Breadth-First Search (BFS) and Depth-First Search (DFS) algorithms. The results are displayed dynamically using a web interface.

### Prerequisites

Before starting, ensure you have **Python 3.7+** installed on your machine. You can verify this by running:

```bash
python --version
```

### Step-by-step Installation

1. **Clone the repository** (if applicable):

   ```bash
   git clone https://github.com/ricardious/InteractiveGraphVisualizer.git
   cd InteractiveGraphVisualizer
   ```

2. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies**:

   Run the following command to install all the necessary packages from the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

   The dependencies are:
   - **PyQt5**: For creating the graphical user interface.
   - **NetworkX**: To manage the graph data structure and apply algorithms.
   - **PyVis**: For rendering the graph visualization in a web view.

4. **Run the application**:

   Once all the dependencies are installed, you can run the project by executing:

   ```bash
   python main.py
   ```

   This will launch the interactive graph visualizer where you can add vertices, edges, and run BFS or DFS algorithms on the graph.
