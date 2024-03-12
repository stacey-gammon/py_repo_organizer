import os
import sys


sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("../src"))

from scripts.visualize.args import VisualizeArgsParser

from src.types import VisualizerConfig
from src.context import Ctx
from src.py_repo_organizer import PyRepoOrganizer
from src.logger import Logger

if __name__ == '__main__':
    args = VisualizeArgsParser.get_cli_args()
    ctx = Ctx(logger=Logger(log_level=args.log_level))
    visualize_config = VisualizerConfig(output_folder=args.output_folder, layout=args.layout)
    PyRepoOrganizer.visualize(ctx, package=args.project_path, folder=args.folder, visualizer_config=visualize_config)
