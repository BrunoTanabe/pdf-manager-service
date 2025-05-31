from enum import Enum


class PDFType(Enum):
    """Enum para tipos de PDF suportados."""

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    UNKNOWN = "UNKNOWN"
