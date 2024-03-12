from dataclasses import dataclass, field

@dataclass
class Import:
    importer: str
    imported: str

    def __eq__(self, other):
        if not isinstance(other, Import):
            return False
        return self.importer == other.importer and self.imported == other.imported

    def __hash__(self):
        return hash((self.importer, self.imported))


@dataclass
class CodeNodeAnalysis:
    """
    Represents some analysis on a group of code, whether it's a file, a deeply nested folder, or a high-level folder.
    """

    id: str
    """
    A representation of the code node, using dot notation, which should be unique within the context of the repository.
    Examples:
    `foo.bar`
    `foo.bar.zed`
    """

    dependency_connections: dict[str, set[Import]] = field(default_factory=dict)
    """
    A list of dependencies this code node has on another, and the number of times the dependency occurs. For example,
    if this is a file node, and the dependency is a folder, and this file imports code from that folder two times, the
    import list will contain two imports.
    """


