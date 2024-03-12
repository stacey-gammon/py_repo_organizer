from src.context import Ctx
from src.internals.types import CodeNodeAnalysis


class PrettyPrinter:
    @staticmethod
    def print_sccs(ctx: Ctx, *, sccs: list[set[str]], code_analysis_cache: dict[str, CodeNodeAnalysis]) -> None:
        """
        Prints the strongly connected components.
        """
        ctx.logger.info("Strongly connected components:")



        for scc in sccs:
            if len(scc) <= 1:
                continue

            PrettyPrinter._print_scc(ctx, scc, code_analysis_cache)
            ctx.logger.info("\n")

    @staticmethod
    def _print_scc(ctx: Ctx, scc: set[str], code_analysis_cache: dict[str, CodeNodeAnalysis]) -> None:
        """
        Prints the given strongly connected component.
        """
        ctx.logger.info(f"{len(scc)} length SCC:")
        for node in scc:
            ctx.logger.info(f"\t{node}")
            code_analysis = code_analysis_cache.get(node)
            for dependency in code_analysis.dependency_connections:
                if dependency in scc:
                    ctx.logger.info(f"\t\t{node} -> {dependency}:")
                    for import_info in code_analysis.dependency_connections[dependency]:
                        ctx.logger.info(f"\t\t\t{import_info.importer} -> {import_info.imported}")
        ctx.logger.info("\n")
