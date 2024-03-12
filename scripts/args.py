import argparse
from dataclasses import dataclass
from src.logger import LogLevel


@dataclass
class Args:
    project_path: str
    log_level: LogLevel
    folder: str


@dataclass
class ArgsParser:
    @staticmethod
    def get_cli_arg_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            prog="ProgramName",
            description="What the program does",
            epilog="Text at the bottom of help",
        )
        parser.add_argument(
            "--path", help="The path to the python project."
        )
        parser.add_argument(
            "--folder", help="Filter on a specific sub folder, relative to the project path."
        )
        parser.add_argument(
            "--log", help="Log level", default="INFO"
        )

        return parser

    @staticmethod
    def get_cli_args() -> Args:
        parser = ArgsParser.get_cli_arg_parser()
        return Args(
            project_path=parser.parse_args().path,
            folder=parser.parse_args().folder or "",
            log_level=ArgsParser._parse_log_level(parser.parse_args().log)
        )

    @staticmethod
    def parse_args(parser: argparse.ArgumentParser) -> Args:
        return Args(
            project_path=parser.parse_args().path,
            folder=parser.parse_args().folder or "",
            log_level=ArgsParser._parse_log_level(parser.parse_args().log)
        )

    @staticmethod
    def _parse_log_level(log_level: str) -> LogLevel:
        if log_level == "DEBUG":
            return LogLevel.DEBUG
        elif log_level == "INFO":
            return LogLevel.INFO
        elif log_level == "WARN":
            return LogLevel.WARN
        elif log_level == "ERROR":
            return LogLevel.ERROR
        else:
            raise ValueError(f"Invalid log level: {log_level}")
