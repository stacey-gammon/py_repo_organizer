import os
import sys

from src.context import Ctx

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../src"))

from src.py_repo_organizer import PyRepoOrganizer
from src.logger import Logger

from scripts.args import ArgsParser

if __name__ == '__main__':
    args = ArgsParser.get_cli_args()
    logger = Logger(log_level=args.log_level)
    ctx = Ctx(logger=logger)
    PyRepoOrganizer.print_break_circle_suggestions(ctx=ctx, package_root=args.project_path, folder_filter=args.folder_filter, logger=logger)
