from dataclasses import dataclass

from src.entities.enums.pdf_page_type import PDFPageType


@dataclass
class PDFPageResult:
    """Estrutura de dados para análise de página"""
    page_number: int
    page_type: PDFPageType
    text_length: int
    image_count: int
    image_coverage: float
    has_meaningful_text: bool
    has_high_image_coverage: bool