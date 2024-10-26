from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTextEdit,
    QGroupBox,
    QMessageBox,
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
import networkx as nx
from pyvis.network import Network
import tempfile
import os
from graph_algorithms.bfs import bfs
from graph_algorithms.dfs import dfs


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador Interactivo de Grafos")
        self.graph = nx.Graph()
        self.temp_dir = tempfile.mkdtemp()
        self.html_path = os.path.join(self.temp_dir, "graph.html")
        self.result_html_path = os.path.join(self.temp_dir, "result_graph.html")
        self.setup_ui()

    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo para controles
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Grupo de entrada de datos
        input_group = QGroupBox("Entrada de datos")
        input_layout = QVBoxLayout()

        # Entrada de vértice
        vertex_layout = QHBoxLayout()
        vertex_layout.addWidget(QLabel("Vértice:"))
        self.vertex_entry = QLineEdit()
        vertex_layout.addWidget(self.vertex_entry)
        self.add_vertex_btn = QPushButton("Agregar Vértice")
        self.add_vertex_btn.clicked.connect(self.add_vertex)
        vertex_layout.addWidget(self.add_vertex_btn)
        input_layout.addLayout(vertex_layout)

        # Entrada de arista
        edge_layout = QHBoxLayout()
        edge_layout.addWidget(QLabel("Arista (A--B):"))
        self.edge_entry = QLineEdit()
        edge_layout.addWidget(self.edge_entry)
        self.add_edge_btn = QPushButton("Agregar Arista")
        self.add_edge_btn.clicked.connect(self.add_edge)
        edge_layout.addWidget(self.add_edge_btn)
        input_layout.addLayout(edge_layout)

        # Selector de algoritmo
        algo_layout = QHBoxLayout()
        algo_layout.addWidget(QLabel("Algoritmo:"))
        self.algorithm_combo = QComboBox()
        self.algorithm_combo.addItems(["BFS", "DFS"])
        algo_layout.addWidget(self.algorithm_combo)
        self.run_algorithm_btn = QPushButton("Ejecutar Algoritmo")
        self.run_algorithm_btn.clicked.connect(self.run_algorithm)
        algo_layout.addWidget(self.run_algorithm_btn)
        input_layout.addLayout(algo_layout)

        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)

        # Información del grafo
        info_group = QGroupBox("Información del Grafo")
        info_layout = QVBoxLayout()
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        info_layout.addWidget(self.info_text)
        info_group.setLayout(info_layout)
        left_layout.addWidget(info_group)

        main_layout.addWidget(left_panel)

        # Panel derecho para visualización de grafos (dos columnas)
        right_panel = QWidget()
        right_layout = QHBoxLayout(right_panel)

        # Primera columna para el grafo original
        self.web_view = QWebEngineView()
        self.web_view.setFixedWidth(600)  # Ajustar ancho al 50%
        right_layout.addWidget(self.web_view)

        # Segunda columna para el resultado del algoritmo
        self.result_web_view = QWebEngineView()
        self.result_web_view.setFixedWidth(600)  # Ajustar ancho al 50%
        right_layout.addWidget(self.result_web_view)

        main_layout.addWidget(right_panel)

        # Ajustar tamaño de la ventana
        self.setMinimumSize(1200, 800)

        # Inicializar visualización vacía
        self.update_visualization()

    def add_vertex(self):
        vertex = self.vertex_entry.text().strip()
        if vertex:
            if vertex not in self.graph:
                self.graph.add_node(vertex)
                self.vertex_entry.clear()
                self.update_visualization()
                self.update_info()
            else:
                QMessageBox.warning(self, "Advertencia", "El vértice ya existe!")

    def add_edge(self):
        edge = self.edge_entry.text().strip()
        if edge and "--" in edge:
            v1, v2 = edge.split("--")
            v1, v2 = v1.strip(), v2.strip()
            if v1 in self.graph and v2 in self.graph:
                self.graph.add_edge(v1, v2)
                self.edge_entry.clear()
                self.update_visualization()
                self.update_info()
            else:
                QMessageBox.warning(
                    self, "Advertencia", "Uno o ambos vértices no existen!"
                )

    def update_visualization(self, visited_order=None):
        # Crear red PyVis para el grafo original
        net = Network(height="600px", width="100%", bgcolor="#ffffff")

        # Agregar nodos y aristas manualmente
        for node in self.graph.nodes():
            net.add_node(node)

        for edge in self.graph.edges():
            net.add_edge(edge[0], edge[1])

        # Guardar y mostrar grafo original
        try:
            net.write_html(self.html_path)
            self.web_view.setUrl(QUrl.fromLocalFile(self.html_path))
        except Exception as e:
            QMessageBox.warning(
                self, "Error", f"Error al guardar la visualización: {str(e)}"
            )

        # Si hay un orden de visita, crear una segunda visualización para el resultado del algoritmo
        if visited_order:
            result_net = Network(height="600px", width="100%", bgcolor="#ffffff")

            # Agregar nodos y aristas del grafo con el resultado del algoritmo
            for node in self.graph.nodes():
                result_net.add_node(node)

            for edge in self.graph.edges():
                result_net.add_edge(edge[0], edge[1])

            # Colorear los nodos según el orden de visita
            for i, node in enumerate(visited_order):
                # Calcular color en escala de azul según orden de visita
                color = (
                    f"#{int(255 * (1 - i/len(visited_order))):02x}"
                    + f"{int(255 * (1 - i/len(visited_order))):02x}ff"
                )
                # Modificar el nodo para agregarle color
                for n in result_net.nodes:
                    if n["id"] == node:
                        n["color"] = color

            # Guardar y mostrar grafo con el resultado
            try:
                result_net.write_html(self.result_html_path)
                self.result_web_view.setUrl(QUrl.fromLocalFile(self.result_html_path))
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Error al guardar la visualización del resultado: {str(e)}",
                )

    def run_algorithm(self):
        if not self.graph.nodes():
            QMessageBox.warning(self, "Advertencia", "El grafo está vacío!")
            return

        start_vertex = list(self.graph.nodes())[0]  # Usar el primer vértice como inicio

        if self.algorithm_combo.currentText() == "BFS":
            visited_order = bfs(self.graph, start_vertex)
        else:  # DFS
            visited_order = dfs(self.graph, start_vertex)

        self.update_visualization(visited_order)

    def update_info(self):
        info = f"Vértices: {list(self.graph.nodes())}\n"
        info += f"Aristas: {list(self.graph.edges())}\n"
        self.info_text.setText(info)

    def closeEvent(self, event):
        # Limpiar archivos temporales al cerrar
        try:
            os.remove(self.html_path)
            os.remove(self.result_html_path)
            os.rmdir(self.temp_dir)
        except:
            pass
        super().closeEvent(event)
