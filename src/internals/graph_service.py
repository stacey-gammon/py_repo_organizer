from typing import Optional

import grimp
import networkx as nx
from grimp import ImportGraph
from networkx import DiGraph

from src.context import Ctx
from src.internals.graphing.graph_utils import GraphUtils


class GraphService:
    @staticmethod
    def get_sccs(ctx: Ctx, *, graph: DiGraph) -> list[set[str]]:
        """
        Given the graph, returns the strongly connected components.
        """
        sccs = nx.strongly_connected_components(graph)
        return [{str(s) for s in scc} for scc in sccs]


    @staticmethod
    def build_graph(ctx: Ctx, *, package_name: str, folder: str) -> DiGraph:
        """
        """
        module_level_grimp_graph = GraphUtils.build_grimp_graph(ctx, package_name=package_name)

        digraph = GraphUtils.di_graph_from_grimp_graph(ctx, import_graph=module_level_grimp_graph)
        ctx.logger.debug(f"Module-level graph has {len(digraph.nodes)} nodes and {len(digraph.edges)} edges.")
        return GraphUtils.filter_graph_on_folder(ctx, graph=digraph, folder=folder)

    @staticmethod
    def get_top_level_graph(ctx: Ctx, *, graph: nx.DiGraph) -> DiGraph:
        """
        Only keeps the nodes that are top-level of the graph.

        Should use the `expanded_graph` to make sure the dependencies are correct.
        """
        new_graph = DiGraph()
        for node in graph.nodes:
            # Only keep node ids that have no "." in them which means they are the top level.
            if "." not in node:
                new_graph.add_node(node)

        for edge in graph.edges:
            if edge[0] in new_graph.nodes and edge[1] in new_graph.nodes:
                new_graph.add_edge(edge[0], edge[1])

        ctx.logger.debug(f"Reduced graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges "
                f"to {len(new_graph.nodes)} nodes and {len(new_graph.edges)} edges after filtering on top-level.")

        return new_graph
