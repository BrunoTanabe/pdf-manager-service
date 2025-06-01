import logging
import re

import fitz

from src.boundaries.pdf_image_coverage import PDFImageCoverage
from src.entities.dataclasses.pdf_config import PDFConfig
from src.entities.dataclasses.pdf_page_analysis import PDFPageAnalysis
from src.entities.enums.pdf_page_type import PDFPageType

# Configuração de logging
logger = logging.getLogger(__name__)


class PDFPageAnalyzer:
    """Classe responsável pela análise individual de páginas PDF."""

    def __init__(self, config: PDFConfig):
        self.config = config
        self.image_calculator = PDFImageCoverage(config)

    def analyze_page(self, page: fitz.Page, page_number: int) -> PDFPageAnalysis:
        """
        Analisa uma página específica do PDF.

        Args:
            page: Página do PDF
            page_number: Número da página (1-indexed)

        Returns:
            PageAnalysis: Resultado da análise da página
        """
        page_area = page.rect.width * page.rect.height

        # Extrair e limpar texto
        raw_text = page.get_text().strip()
        clean_text = re.sub(r"\s+", " ", raw_text)

        # Calcular cobertura de imagens
        image_coverage = self.image_calculator.calculate_coverage(page, page_area)

        # Obter lista de imagens
        image_list = page.get_images()

        # Determinar características da página
        has_meaningful_text = len(clean_text) > self.config.min_text_threshold
        has_high_image_coverage = image_coverage > self.config.max_image_coverage
        has_images = len(image_list) > 0

        # Para páginas sem texto significativo, verificar se há pelo menos algum conteúdo visual
        if not has_meaningful_text and not has_images:
            # Pode ser uma página com elementos gráficos que não são detectados como imagens
            # Verificar se há pelo menos algum conteúdo na página
            drawings = page.get_drawings()
            if drawings or page_area > 0:
                has_images = True  # Tratar como conteúdo visual

        # Determinar tipo da página
        page_type = self._determine_page_type(
            has_meaningful_text, has_high_image_coverage, has_images
        )

        return PDFPageAnalysis(
            page_number=page_number,
            type=page_type,
            text_length=len(clean_text),
            image_count=len(image_list),
            image_coverage=round(image_coverage, 3),
            has_meaningful_text=has_meaningful_text,
            has_high_image_coverage=has_high_image_coverage,
            clean_text=clean_text,
        )

    def _determine_page_type(
        self,
        has_meaningful_text: bool,
        has_high_image_coverage: bool,
        has_images: bool,
    ) -> PDFPageType:
        """Determina o tipo da página baseado em suas características."""
        if has_meaningful_text and not has_high_image_coverage:
            return PDFPageType.TEXT
        elif has_high_image_coverage or (has_images and not has_meaningful_text):
            return PDFPageType.IMAGE
        elif has_meaningful_text and has_images:
            return PDFPageType.MIXED
        elif has_images:  # Páginas com imagens mas sem texto significativo
            return PDFPageType.IMAGE
        else:
            return PDFPageType.UNKNOWN
