import logging
from typing import List, Optional

import fitz

from src.controls.pdf_exception import PDFAnalysisException
from src.entities.dataclasses.pdf_config import PDFConfig

# Configuração de logging
logger = logging.getLogger(__name__)


class PDFImageCoverage:
    """Classe responsável pelo cálculo da cobertura de imagens em páginas PDF."""

    def __init__(self, config: PDFConfig):
        self.config = config

    def calculate_coverage(self, page: fitz.Page, page_area: float) -> float:
        """
        Calcula a cobertura de imagens em uma página.

        Args:
            page: Página do PDF
            page_area: Área total da página

        Returns:
            float: Percentual de cobertura de imagens (0.0 a 1.0)

        Raises:
            PDFAnalysisError: Se houver erro no cálculo da cobertura
        """
        try:
            image_list = page.get_images()
            if not image_list:
                return 0.0

            total_image_area = 0.0

            for img_index, img in enumerate(image_list):
                try:
                    image_area = self._calculate_single_image_area(page, img, page_area)
                    total_image_area += image_area
                except Exception as e:
                    logger.warning(f"Erro ao calcular área da imagem {img_index}: {e}")
                    # Usar área padrão como fallback
                    default_area = page_area * 0.2
                    total_image_area += default_area

            coverage = min(total_image_area / page_area, 1.0) if page_area > 0 else 0.0
            return coverage

        except Exception as e:
            logger.error(f"Erro ao calcular cobertura de imagens: {e}")
            raise PDFAnalysisException(f"Falha no cálculo de cobertura de imagens: {e}")

    def _calculate_single_image_area(
        self, page: fitz.Page, img: tuple, page_area: float
    ) -> float:
        """
        Calcula a área de uma única imagem usando múltiplas estratégias.

        Args:
            page: Página do PDF
            img: Tupla com informações da imagem
            page_area: Área total da página

        Returns:
            float: Área da imagem
        """
        xref = img[0]
        image_instances = []

        # Estratégia 1: Usar get_image_bbox
        image_instances.extend(self._get_image_bbox(page, img))

        # Estratégia 2: Procurar através do conteúdo da página
        if not image_instances:
            image_instances.extend(self._get_image_from_page_dict(page))

        # Estratégia 3: Estimativa baseada em dimensões
        if not image_instances:
            estimated_bbox = self._estimate_image_bbox(page, xref)
            if estimated_bbox:
                image_instances.append(estimated_bbox)

        # Calcular área total das instâncias encontradas
        total_area = 0.0
        for bbox in image_instances:
            area = bbox.width * bbox.height
            if area > 0:
                total_area += area

        # Se não conseguiu calcular, usar área padrão
        if total_area == 0:
            total_area = min(
                page_area * self.config.max_default_image_area_ratio, page_area
            )

        return total_area

    def _get_image_bbox(self, page: fitz.Page, img: tuple) -> List[fitz.Rect]:
        """Tenta obter bbox da imagem usando get_image_bbox."""
        try:
            bbox = page.get_image_bbox(img)
            if bbox and bbox != fitz.Rect():
                return [bbox]
        except Exception as e:
            logger.debug(f"Falha ao obter bbox da imagem: {e}")
        return []

    def _get_image_from_page_dict(self, page: fitz.Page) -> List[fitz.Rect]:
        """Procura imagens através do dicionário da página."""
        image_instances = []
        try:
            page_dict = page.get_text("dict")
            if "blocks" in page_dict:
                for block in page_dict["blocks"]:
                    if block.get("type") == 1:  # Tipo 1 = bloco de imagem
                        bbox = fitz.Rect(block["bbox"])
                        image_instances.append(bbox)
        except Exception as e:
            logger.debug(f"Falha ao obter imagens do dicionário da página: {e}")
        return image_instances

    def _estimate_image_bbox(self, page: fitz.Page, xref: int) -> Optional[fitz.Rect]:
        """Estima bbox da imagem baseado em suas dimensões."""
        try:
            pix = fitz.Pixmap(page.parent, xref)
            if not pix:
                return None

            img_width = pix.width
            img_height = pix.height

            scale_x = (
                min(page.rect.width * self.config.image_scale_factor, img_width)
                / img_width
            )
            scale_y = (
                min(
                    page.rect.height * self.config.image_scale_factor,
                    img_height,
                )
                / img_height
            )
            scale = min(scale_x, scale_y)

            estimated_width = img_width * scale
            estimated_height = img_height * scale

            x0 = (page.rect.width - estimated_width) / 2
            y0 = (page.rect.height - estimated_height) / 2
            x1 = x0 + estimated_width
            y1 = y0 + estimated_height

            pix = None  # Liberar memória
            return fitz.Rect(x0, y0, x1, y1)

        except Exception as e:
            logger.debug(f"Falha ao estimar bbox da imagem: {e}")
            return None
