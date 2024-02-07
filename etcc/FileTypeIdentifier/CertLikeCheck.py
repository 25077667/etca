from .FileTypeCheck import FileTypeCheck


class CertLikeCheck(FileTypeCheck):
    def check(self, path: str) -> set:
        result = set()
        cert_extensions = [".pem", ".cer", ".crt", ".der"]
        if any(path.lower().endswith(ext) for ext in cert_extensions):
            result.add("certificate")
        return result
