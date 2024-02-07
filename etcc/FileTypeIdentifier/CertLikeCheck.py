from .FileTypeCheck import FileTypeCheck


class CertLikeCheck(FileTypeCheck):
    def check(self, path: str) -> str:
        cert_extensions = [".pem", ".cer", ".crt", ".der"]
        if any(path.lower().endswith(ext) for ext in cert_extensions):
            return "Certificate-like"
        return None
