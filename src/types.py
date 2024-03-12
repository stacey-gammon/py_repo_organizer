from dataclasses import dataclass


@dataclass
class VisualizerConfig:
    image_type: str = "svg"
    file_name: str = "graph"
    layout: str = "dot"
    output_folder: str = "."
