from dataclasses import dataclass

from src.entities.enums.pdf_page_type import PDFPageType


@dataclass
class PDFPageAnalysis:
    """Resultado da análise de uma página específica."""

    page_number: int
    type: PDFPageType
    text_length: int
    image_count: int
    image_coverage: float
    has_meaningful_text: bool
    has_high_image_coverage: bool
    clean_text: str = ""
