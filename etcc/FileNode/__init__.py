from typing import AnyStr, MutableSet


class FileNode:
    @staticmethod
    def __make_detail_types() -> MutableSet[str]:
        return set()

    def __init__(
        self, path: AnyStr = "", detail_types: MutableSet[str] = __make_detail_types()
    ):
        self.path = path
        self.detail_types = detail_types

    def __str__(self) -> str:
        detial_types = ", ".join(self.detail_types)
        return f"{self.path}: {detial_types}"

    def to_dict(self) -> dict:
        """
        Convert the FileNode instance into a dictionary for JSON serialization.
        """
        # Convert FrozenSet to list for serialization
        return {"path": self.path, "detail_types": list(self.detail_types)}

    def __eq__(self, other) -> bool:
        return self.path == other.path

    def __hash__(self) -> int:
        return hash(self.path)
