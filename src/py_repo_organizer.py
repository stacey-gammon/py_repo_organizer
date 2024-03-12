import os
import sys
from typing import Optional

from networkx import DiGraph

from src.context import Ctx
from src.internals.analyzer_service import AnalyzerService
from src.internals.graph_service import GraphService
from src.types import VisualizerConfig
from src.internals.visualizer_service import VisualizerService
from src.logger import Logger
from src.internals.pretty_printer import PrettyPrinter


class PyRepoOrganizer:

    @staticmethod
    def analyze_project(ctx: Ctx, *, package_root: str, logger: Logger, folder: Optional[str] = None) -> None:
        """
        Analyze the given project and print the results to the console.
        """
        pass


    @staticmethod
    def visualize(ctx: Ctx, *, package: str, folder: str, visualizer_config: VisualizerConfig) -> None:
        import_graph = AnalyzerService.get_project_import_graph(ctx, package=package, folder=folder)
        code_analysis_cache, expanded_graph = AnalyzerService.analyze_graph(ctx, graph=import_graph)
        top_level_graph = GraphService.get_top_level_graph(ctx, graph=expanded_graph)
        VisualizerService.visualize_graph(ctx, config=visualizer_config, graph=top_level_graph)

        sccs = GraphService.get_sccs(ctx, graph=top_level_graph)
        PrettyPrinter.print_sccs(ctx, sccs=sccs, code_analysis_cache=code_analysis_cache)

    @staticmethod
    def print_sccs(ctx: Ctx, *, package: str, folder: str = "") -> None:
        import_graph = AnalyzerService.get_project_import_graph(ctx, package=package, folder=folder)

        code_analysis_cache, expanded_graph = AnalyzerService.analyze_graph(ctx, graph=import_graph)
        sccs = GraphService.get_sccs(ctx, graph=expanded_graph)
        PrettyPrinter.print_sccs(ctx, sccs=sccs)

