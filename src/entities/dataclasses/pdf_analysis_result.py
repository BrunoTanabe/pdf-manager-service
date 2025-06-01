from dataclasses import dataclass
from typing import List

from src.entities.dataclasses.pdf_page_analysis import PDFPageAnalysis
from src.entities.enums.pdf_type import PDFType


@dataclass
class PDFAnalysisResult:
    """Resultado completo da análise do PDF."""

    pdf_type: PDFType
    total_pages: int
    text_pages: int
    image_pages: int
    total_text_length: int
    average_image_coverage: float
    pages_analysis: List[PDFPageAnalysis]
