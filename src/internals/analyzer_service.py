import os
import sys
from typing import Optional, Tuple

from networkx import DiGraph

from src.context import Ctx
from src.internals.graph_service import GraphService
from src.internals.types import CodeNodeAnalysis, Import


class AnalyzerService:
    @staticmethod
    def analyze_graph(ctx: Ctx, graph: DiGraph) -> Tuple[dict[str, CodeNodeAnalysis], DiGraph]:
        """
        Analyzes the given graph and returns the results.
        """
        code_analysis_cache: dict[str, CodeNodeAnalysis] = {}
        """
        Will eventually contain a CodeNodeAnalysis for each node in the graph, keyed by id.
        """

        # First analyze all the files, then we will handle rolling up each CodeNodeAnalysis to its parent.
        expanded_graph = DiGraph()
        for node in graph.nodes:
            AnalyzerService._analyze_file_node(ctx, node, graph, expanded_graph, code_analysis_cache)
        return code_analysis_cache, expanded_graph

    @staticmethod
    def get_project_import_graph(ctx: Ctx, *, package: str, folder: Optional[str] = None) -> DiGraph:
        """
        Analyze the given project and print the results to the console.
        """
        package_name = os.path.basename(package)
        # Now get the path without the root folder name
        project_path = package[:-len(package_name)]

        # I think we have to add the project path to the sys path so that we can import the modules and relative import
        # paths work.
        sys.path.insert(0, os.path.abspath(project_path))

        return GraphService.build_graph(ctx, package_name=package_name, folder=folder)


    @staticmethod
    def _analyze_file_node(
            ctx: Ctx, node_id: str, graph: DiGraph, expanded_graph: DiGraph, code_analysis_cache: dict[str, CodeNodeAnalysis]) -> CodeNodeAnalysis:
        node_ancestors = AnalyzerService._get_ancestor_paths(node_id) + [node_id]

        for dependency in graph.successors(node_id):
            import_info = Import(importer=node_id, imported=dependency)

            # Add the import connection to every level of the ancestor.
            for ancestor in node_ancestors:
                ancestor_analysis = AnalyzerService.get_code_analysis(ancestor, code_analysis_cache)
                dependency_ancestors = AnalyzerService._get_ancestor_paths(dependency) + [dependency]
                for dependency_ancestor in dependency_ancestors:
                    if dependency_ancestor == ancestor:
                        continue
                    if dependency_ancestor not in ancestor_analysis.dependency_connections:
                        ancestor_analysis.dependency_connections[dependency_ancestor] = set()
                    ancestor_analysis.dependency_connections[dependency_ancestor].add(import_info)
                    expanded_graph.add_edge(ancestor, dependency_ancestor)

        return AnalyzerService.get_code_analysis(node_id, code_analysis_cache)

    @staticmethod
    def get_code_analysis(node_id: str, code_analysis_cache: dict[str, CodeNodeAnalysis]) -> CodeNodeAnalysis:
        if node_id not in code_analysis_cache:
            code_analysis_cache[node_id] = CodeNodeAnalysis(id=node_id)
        return code_analysis_cache[node_id]

    @staticmethod
    def _get_ancestor_paths(path: str) -> list[str]:
        """
        Returns a list of ancestor paths for the given path. For example, if the path is `foo.bar.zed`, this will return
        `['foo', 'foo.bar', 'foo.bar.zed']`.
        """
        ancestor_paths = []
        parts = path.split(".")
        for i in range(1, len(parts) + 1):
            ancestor_paths.append(".".join(parts[:i]))
        return ancestor_paths

