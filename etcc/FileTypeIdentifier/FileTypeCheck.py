"""Module for checking file types."""


class FileTypeCheck:
    """Base class for checking file types."""

    def __init__(self):
        pass

    def check(self, path: str) -> str:
        """Method to be implemented by subclasses for checking file types."""
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        return self.__class__.__name__
