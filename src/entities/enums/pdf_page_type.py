from enum import Enum


class PDFPageType(Enum):
    """Enum para tipos de página dentro de um PDF."""

    TEXT = "TEXT"
    IMAGE = "IMAGE"
    MIXED = "MIXED"
    UNKNOWN = "UNKNOWN"
