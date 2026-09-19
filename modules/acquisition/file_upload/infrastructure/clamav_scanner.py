"""ClamAV antivirus scanner implementation."""

from io import BytesIO

import clamd


class MalwareDetectedError(Exception):
    """Raised when ClamAV detects malware in an uploaded file."""


class ClamAVScanner:
    """Scan uploaded file content using the ClamAV daemon."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3310,
    ) -> None:
        self._client = clamd.ClamdNetworkSocket(
            host=host,
            port=port,
        )

    def scan(self, file_content: bytes) -> None:
        """Scan file content and raise an error if malware is detected."""

        try:
            result = self._client.instream(
                BytesIO(file_content),
            )
        except Exception as exc:
            raise RuntimeError(
                "ClamAV antivirus scan failed."
            ) from exc

        status, signature = result["stream"]

        if status == "FOUND":
            raise MalwareDetectedError(
                f"Malware detected: {signature}"
            )

        if status != "OK":
            raise RuntimeError(
                "ClamAV returned an unexpected scan result."
            )