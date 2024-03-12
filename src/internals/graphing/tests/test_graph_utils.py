from networkx import DiGraph
import pytest

from src.internals.graphing.graph_utils import GraphUtils


class TestGraphUtils:

    def test_filter_graph_on_folder(self) -> None:
        graph = DiGraph()
        graph.add_edge("a.a", "b.c")

        filtered_graph = GraphUtils.filter_graph_on_folder(graph, "a")
        # b is not in a, the edge should not exist.
        assert set(filtered_graph.nodes) == {"a"}
        assert filtered_graph.edges == set()
