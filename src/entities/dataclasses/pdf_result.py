from dataclasses import dataclass
from typing import List

from src.entities.dataclasses.pdf_page_result import PDFPageResult
from src.entities.enums.pdf_type import PDFType


@dataclass
class PDFResult:
    """Informações completas do PDF analisado"""
    pdf_type: PDFType
    total_pages: int
    text_pages: int
    image_pages: int
    mixed_pages: int
    total_text_length: int
    total_image_coverage: float
    pages_analysis: List[PDFPageResult]
    pdf_text: str