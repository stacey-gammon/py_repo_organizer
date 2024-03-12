import os
import subprocess

import networkx as nx

from src.context import Ctx
from src.types import VisualizerConfig


class VisualizerService:
    @staticmethod
    def visualize_graph(ctx: Ctx, *, config: VisualizerConfig, graph: nx.DiGraph) -> None:
        ctx.logger.debug(f"Building visualization for graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges.")
        dot_file_text = VisualizerService._generate_dot_file_text(graph)

        image_type = config.image_type
        layout = config.layout
        path = config.output_folder
        file_name = config.file_name
        os.makedirs(path, exist_ok=True)
        dot_file_path = os.path.join(path, f"{file_name}.dot")

        with open(dot_file_path, "w") as f:
            ctx.logger.info(f"Writing graph dot file to {dot_file_path}...")
            f.write(dot_file_text)

        try:
            ctx.logger.info("Building visualization...")
            image_path = os.path.join(path, f"{file_name}.{image_type}")

            subprocess.run(["dot", f"-T{image_type}", f"-K{layout}", dot_file_path, "-o", image_path])

            ctx.logger.info(f"Visualization created at {image_path}")
        except Exception:
            ctx.logger.error(
                "Failed to generate graph.svg. Is graphviz installed? If not, download it at https://graphviz.org/download/",
            )


    @staticmethod
    def _generate_dot_file_text(graph: nx.DiGraph) -> str:
        """
        Builds a dot file for the given graph.
        """
        label = f"""
        # of Nodes: {len(graph.nodes())}
        # of Edges: {len(graph.edges())}
        """

        intro = "digraph G {"
        text = f"""{intro}
            graph [
                label = "{label}\n\n"
                fontsize = 20
                overlap_scaling=25
            ]
        """

        for node in graph.nodes:
            text += f"\"{node}\"\n"

        text += "\n\n"

        color = "black"
        for edge in graph.edges:
            text += f'"{edge[0]}" -> "{edge[1]}" [color = "{color}"]\n'

        text += "}"
        return text
