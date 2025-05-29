from enum import Enum

class PDFPageType(Enum):
    """Enum para tipos de página"""
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    UNKNOWN = "UNKNOWN"