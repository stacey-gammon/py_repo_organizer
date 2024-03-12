import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../src"))

from src.context import Ctx
from src.py_repo_organizer import PyRepoOrganizer
from src.logger import Logger

from scripts.args import ArgsParser

if __name__ == '__main__':
    args = ArgsParser.get_cli_args()
    ctx = Ctx(logger=Logger(log_level=args.log_level))
    PyRepoOrganizer.print_sccs(ctx, package=args.project_path, folder=args.folder_filter or "")
