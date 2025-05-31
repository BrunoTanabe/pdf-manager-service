import logging
from pathlib import Path
from typing import Optional

import fitz
from pdfminer.pdfpage import PDFPage

from src.boundaries.pdf_page_analyzer import PDFPageAnalyzer
from src.controls.pdf_exception import (
    PDFAnalysisException,
    PDFExtractionException,
)
from src.entities.dataclasses.pdf_analysis_result import PDFAnalysisResult
from src.entities.dataclasses.pdf_config import PDFConfig
from src.entities.enums.pdf_page_type import PDFPageType
from src.entities.enums.pdf_type import PDFType

"""
PDF Service Module

Este módulo fornece funcionalidades para análise e extração de texto de documentos PDF,
incluindo detecção do tipo de PDF (baseado em texto ou imagem) e extração de conteúdo textual.
"""

# Configuração de logging
logger = logging.getLogger(__name__)


class PDFService:
    """
    Serviço principal para análise e extração de texto de documentos PDF.

    Este serviço oferece funcionalidades para:
    - Detectar se um PDF é baseado em texto ou imagem
    - Extrair texto de PDFs
    - Analisar páginas individuais
    """

    def __init__(self, config: Optional[PDFConfig] = None):
        """
        Inicializa o serviço PDF.

        Args:
            config: Configurações personalizadas. Se None, usa configurações padrão.
        """
        self.config = config or PDFConfig()
        self.page_analyzer = PDFPageAnalyzer(self.config)

    def detect_pdf_type(self, pdf_file: str) -> PDFType:
        """
        Detecta o tipo principal do PDF.

        Args:
            pdf_file: Caminho para o arquivo PDF

        Returns:
            PDFType: Tipo detectado do PDF

        Raises:
            PDFAnalysisError: Se houver erro na análise do PDF
            FileNotFoundError: Se o arquivo não existir
        """
        analysis_result = self.analyze_pdf(pdf_file)
        return analysis_result.pdf_type

    def analyze_pdf(self, pdf_file: str) -> PDFAnalysisResult:
        """
        Realiza análise completa do PDF.

        Args:
            pdf_file: Caminho para o arquivo PDF

        Returns:
            PDFAnalysisResult: Resultado completo da análise

        Raises:
            PDFAnalysisError: Se houver erro na análise do PDF
            FileNotFoundError: Se o arquivo não existir
        """
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_file}")

        try:
            # Análise detalhada sempre - a verificação de fonte será usada apenas como hint
            with fitz.open(pdf_file) as doc:
                has_font_resources = self._has_font_resources(pdf_file)
                return self._analyze_document(doc, has_font_resources)

        except Exception as e:
            logger.error(f"Erro na análise do PDF {pdf_file}: {e}")
            raise PDFAnalysisException(f"Falha na análise do PDF: {e}")

    def extract_pdf_text(self, pdf_file: str) -> str:
        """
        Extrai todo o texto do PDF.

        Args:
            pdf_file: Caminho para o arquivo PDF

        Returns:
            str: Texto extraído do PDF

        Raises:
            PDFExtractionError: Se houver erro na extração
            FileNotFoundError: Se o arquivo não existir
        """
        pdf_path = Path(pdf_file)
        if not pdf_path.exists():
            raise FileNotFoundError(f"Arquivo PDF não encontrado: {pdf_file}")

        try:
            with fitz.open(pdf_file) as pdf_doc:
                full_text_parts = []

                for page_num in range(len(pdf_doc)):
                    page = pdf_doc.load_page(page_num)
                    page_text = self._extract_page_text(page)
                    if page_text.strip():
                        full_text_parts.append(page_text)

                return "\n".join(full_text_parts).strip()

        except Exception as e:
            logger.error(f"Erro na extração de texto do PDF {pdf_file}: {e}")
            raise PDFExtractionException(f"Falha na extração de texto: {e}")

    def _has_font_resources(self, pdf_file: str) -> bool:
        """Verifica se o PDF possui recursos de fonte."""
        try:
            with open(pdf_file, "rb") as f:
                for page in PDFPage.get_pages(f):
                    if "Font" in page.resources.keys():
                        return True
            return False
        except Exception as e:
            logger.warning(f"Erro ao verificar recursos de fonte: {e}")
            return True  # Assumir que tem fonte em caso de erro

    def _analyze_document(
        self, doc: fitz.Document, has_font_resources: bool = True
    ) -> PDFAnalysisResult:
        """
        Analisa o documento PDF completo.

        Args:
            doc: Documento PDF aberto
            has_font_resources: Se o PDF possui recursos de fonte
        """
        total_pages = len(doc)
        text_pages = 0
        image_pages = 0
        mixed_pages = 0
        total_text_length = 0
        total_image_coverage = 0.0
        pages_analysis = []

        for page_num in range(total_pages):
            page = doc[page_num]
            page_analysis = self.page_analyzer.analyze_page(page, page_num + 1)
            pages_analysis.append(page_analysis)

            # Contabilizar estatísticas
            total_text_length += page_analysis.text_length
            total_image_coverage += page_analysis.image_coverage

            if page_analysis.type == PDFPageType.TEXT:
                text_pages += 1
            elif page_analysis.type == PDFPageType.IMAGE:
                image_pages += 1
            elif page_analysis.type == PDFPageType.MIXED:
                mixed_pages += 1
                text_pages += 1  # Contar páginas mistas como texto

        # Determinar tipo geral do PDF
        # Se não há recursos de fonte E não há páginas de texto significativas, é IMAGE
        if not has_font_resources and text_pages == 0:
            pdf_type = PDFType.IMAGE
        elif text_pages > image_pages:
            pdf_type = PDFType.TEXT
        elif image_pages > 0:
            pdf_type = PDFType.IMAGE
        else:
            pdf_type = PDFType.UNKNOWN

        # Calcular cobertura média de imagens
        average_image_coverage = (
            total_image_coverage / total_pages if total_pages > 0 else 0.0
        )

        return PDFAnalysisResult(
            pdf_type=pdf_type,
            total_pages=total_pages,
            text_pages=text_pages,
            image_pages=image_pages,
            total_text_length=total_text_length,
            average_image_coverage=round(average_image_coverage, 3),
            pages_analysis=pages_analysis,
        )

    def _extract_page_text(self, page: fitz.Page) -> str:
        """Extrai texto de uma página específica."""
        try:
            text_blocks = page.get_text("blocks")
            page_text_parts = []

            for block in text_blocks:
                if len(block) > 4:  # Verificar se o bloco tem texto
                    block_text = block[4].strip()
                    if block_text:
                        page_text_parts.append(block_text)

            return "\n".join(page_text_parts)

        except Exception as e:
            logger.warning(f"Erro ao extrair texto da página: {e}")
            return ""
