import argparse
from dataclasses import dataclass
from scripts.args import ArgsParser, Args


@dataclass
class VisualizeArgs(Args):
    output_folder: str
    layout: str


@dataclass
class VisualizeArgsParser:
    @staticmethod
    def get_cli_args_parser() -> argparse.ArgumentParser:
        parser = ArgsParser.get_cli_arg_parser()
        parser.add_argument(
            "--output", help="The path to output the graphviz files to."
        )
        parser.add_argument("--layout")
        return parser

    @staticmethod
    def get_cli_args() -> VisualizeArgs:
        parser = VisualizeArgsParser.get_cli_args_parser()

        args = ArgsParser.parse_args(parser)
        return VisualizeArgs(
            folder=args.folder,
            log_level=args.log_level,
            project_path=args.project_path,
            output_folder=parser.parse_args().output,
            layout=parser.parse_args().layout or "dot"
        )
