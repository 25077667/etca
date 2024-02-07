from .FileTypeCheck import FileTypeCheck


class ScriptLikeCheck(FileTypeCheck):
    def check(self, path: str) -> str:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as file:
                first_line = file.readline()

            if first_line.startswith("""#!"""):
                if "bin/bash" in first_line or "bin/sh" in first_line:
                    return "Shell script-like"
                elif "usr/bin/python" in first_line or "bin/python" in first_line:
                    return "Python script-like"
                elif "usr/bin/perl" in first_line or "bin/perl" in first_line:
                    return "Perl script-like"
                elif "usr/bin/ruby" in first_line or "bin/ruby" in first_line:
                    return "Ruby script-like"
                elif "usr/bin/php" in first_line or "bin/php" in first_line:
                    return "PHP script-like"
        except Exception as e:
            print(f"Error reading file: {e}")
        return None
