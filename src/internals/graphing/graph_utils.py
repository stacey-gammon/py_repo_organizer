import grimp
from grimp import ImportGraph
from networkx import DiGraph

from src.context import Ctx


class GraphUtils:

    @staticmethod
    def filter_graph_on_folder(ctx: Ctx, *, graph: DiGraph, folder: str) -> DiGraph:
        filtered_graph = DiGraph()

        module_path = folder.replace("/", ".")
        for node in graph.nodes:
            if not node.startswith(module_path):
                continue

            module_at_folder_root = GraphUtils.trim_folder_from_path(path=node, folder=module_path)
            filtered_graph.add_node(module_at_folder_root)

            for imported in graph.successors(node):
                if not imported.startswith(module_path):
                    continue
                imported_at_folder_root = GraphUtils.trim_folder_from_path(path=imported, folder=module_path)
                filtered_graph.add_edge(module_at_folder_root, imported_at_folder_root)
            for importer in graph.predecessors(node):
                if not importer.startswith(module_path):
                    continue
                importer_at_folder_root = GraphUtils.trim_folder_from_path(path=importer, folder=module_path)
                filtered_graph.add_edge(importer_at_folder_root, module_at_folder_root)

        return filtered_graph


    @staticmethod
    def build_grimp_graph(ctx: Ctx, *, package_name: str) -> ImportGraph:
        ctx.logger.info(f"Building grimp graph...")
        grimp_graph = grimp.build_graph(package_name)
        ctx.logger.info(f"Grimp graph generated")
        return grimp_graph


    @staticmethod
    def di_graph_from_grimp_graph(ctx: Ctx, *, import_graph: ImportGraph) -> DiGraph:
        networkx_graph = DiGraph()

        for module in import_graph.modules:
            networkx_graph.add_node(module)

            for imported in import_graph.find_modules_directly_imported_by(module):
                networkx_graph.add_edge(module, imported)
            for importer in import_graph.find_modules_that_directly_import(module):
                networkx_graph.add_edge(importer, module)

        return networkx_graph

    @staticmethod
    def trim_folder_from_path(path: str, folder: str) -> str:
        trimmed = path[len(folder):]
        if trimmed.startswith("."):
            trimmed = trimmed[1:]
        return trimmed
