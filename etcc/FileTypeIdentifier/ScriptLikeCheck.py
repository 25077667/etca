from .FileTypeCheck import FileTypeCheck


class ScriptLikeCheck(FileTypeCheck):
    COMMON_SHELL_COMMANDS = [
        "awk",
        "bash",
        "cat",
        "chmod",
        "chown",
        "cp",
        "cut",
        "date",
        "echo",
        "find",
        "grep",
        "head",
        "kill",
        "less",
        "ls",
        "mkdir",
    ]
    SHEBANG_MAP = {
        "bin/bash": "Shell script",
        "bin/sh": "Shell script",
        "usr/bin/python": "Python script",
        "bin/python": "Python script",
        "usr/bin/perl": "Perl script",
        "bin/perl": "Perl script",
        "usr/bin/ruby": "Ruby script",
        "bin/ruby": "Ruby script",
        "usr/bin/php": "PHP script",
        "bin/php": "PHP script",
    }

    def __init__(self):
        super().__init__()

    def is_systemd_like(self, path: str) -> bool:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.read()

            # Check for common systemd file extensions
            if path.endswith(".service"):
                return True

            # Look for common systemd configuration patterns
            systemd_indicators = [
                "[Unit]",
                "[Service]",
                "[Install]",
                "[Upload]",
                "[Match]",
                "[Network]",
                "[DHCPv4]",
                "[DHCPv6]",
                "[Journal]",
                "This file is part of systemd.",
                "systemd-analyze cat-config",
            ]

            # Check for the presence of systemd-specific sections or mentions
            if any(indicator in content for indicator in systemd_indicators):
                return True

            return False
        except Exception:
            return False

    def is_shell_like(self, path: str) -> bool:
        if path.endswith(".sh"):
            return True

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                content = file.readlines()
        except Exception as e:
            print(f"Error opening file: {e}")
            return False

        if content and content[0].startswith("#!"):
            if any(sh in content[0] for sh in ["bash", "sh"]):
                return True

        if not all([line.isascii() for line in content[:3]]):
            return False

        # use split to avoid matching "echo" in "echo-123"
        # use generator to avoid creating a list of all commands
        for line in content:
            if any(command in line.split() for command in self.COMMON_SHELL_COMMANDS):
                return True

        # contains lots of "LANG=en_US.UTF-8", "A=B", "export A" etc.
        if all(["=" in line or "export" in line or "LANG" in line for line in content]):
            return True

        return False

    def check(self, path: str) -> list:
        result = set()
        if self.is_systemd_like(path):
            result.add("Systemd")
        if self.is_shell_like(path):
            result.add("Shell script")

        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                first_line = file.readline()
        except Exception as e:
            print(f"Error reading file: {e}")

        if first_line.startswith("#!"):
            for key, value in self.SHEBANG_MAP.items():
                if key in first_line:
                    result.add(value)
                    break

        return result
