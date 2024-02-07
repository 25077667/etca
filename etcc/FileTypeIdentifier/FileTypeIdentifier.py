from . import FileTypeCheck


class FileTypeIdentifier:
    def __init__(self):
        self.checks = []

    def register_check(self, check_instance: FileTypeCheck):
        """Register a new file type check instance."""
        self.checks.append(check_instance)

    def identify(self, path: str) -> frozenset:
        matches = set()
        for check_instance in self.checks:
            result = check_instance.check(path)
            if result:
                matches.add(result)
        return frozenset(matches)
