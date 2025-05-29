from typing import Dict, Optional
import re
from pathlib import Path
import fitz
from pdfminer.pdfpage import PDFPage
import logging

from src.controls.pdf_exception import PDFExtractException, PDFAnalysisException, PDFFileException
from src.entities.dataclasses.pdf_config import PDFConfig
from src.entities.dataclasses.pdf_page_result import PDFPageResult
from src.entities.dataclasses.pdf_result import PDFResult
from src.entities.enums.pdf_page_type import PDFPageType
from src.entities.enums.pdf_type import PDFType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFService:
    """
    Service para análise de PDFs
    Determina se o PDF é baseado em texto ou imagens e extrai informações relevantes
    """

    def __init__(self, config: Optional[PDFConfig] = None):
        """
        Inicializa o service de análise de PDF

        Args:
            config: Configurações para análise (usa padrão se não fornecido)
        """
        self.config = config or PDFConfig()

    def __calculate_image_coverage(self, page, page_area):
        """
        Calcula a porcentagem da página ocupada por imagens

        Args:
            page: Objeto da página do PyMuPDF
            page_area: Área total da página

        Returns:
            float: Porcentagem de cobertura de imagem (0.0 a 1.0)
        """
        image_list = page.get_images()
        total_image_area = 0

        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]

                # Tenta obter o bbox da imagem através dos objetos de página
                # Busca por todas as ocorrências desta imagem na página
                image_instances = []

                # Método 1: Usar get_image_bbox se disponível
                try:
                    bbox = page.get_image_bbox(img)
                    if bbox and bbox != fitz.Rect():
                        image_instances.append(bbox)
                except:
                    pass

                # Método 2: Procurar através do conteúdo da página
                if not image_instances:
                    try:
                        # Analisa o conteúdo da página para encontrar transformações de imagem
                        page_dict = page.get_text("dict")

                        # Procura por blocos de imagem
                        if 'blocks' in page_dict:
                            for block in page_dict['blocks']:
                                if block.get('type') == 1:  # Tipo 1 = bloco de imagem
                                    bbox = fitz.Rect(block['bbox'])
                                    image_instances.append(bbox)
                    except:
                        pass

                # Método 3: Estimativa baseada em dimensões padrão se não encontrar bbox
                if not image_instances:
                    try:
                        # Obtém dimensões da imagem
                        pix = fitz.Pixmap(page.parent, xref)
                        if pix:
                            # Estima posição baseada no tamanho da imagem vs página
                            img_width = pix.width
                            img_height = pix.height

                            # Calcula escala aproximada (assumindo DPI padrão)
                            scale_x = min(page.rect.width * 0.8, img_width) / img_width
                            scale_y = min(page.rect.height * 0.8, img_height) / img_height
                            scale = min(scale_x, scale_y)

                            estimated_width = img_width * scale
                            estimated_height = img_height * scale

                            # Cria bbox estimado (centralizado)
                            x0 = (page.rect.width - estimated_width) / 2
                            y0 = (page.rect.height - estimated_height) / 2
                            x1 = x0 + estimated_width
                            y1 = y0 + estimated_height

                            estimated_bbox = fitz.Rect(x0, y0, x1, y1)
                            image_instances.append(estimated_bbox)

                            pix = None  # Libera memória
                    except:
                        # Se tudo falhar, assume uma área padrão conservadora
                        default_area = min(page_area * 0.3, page_area)  # Máximo 30% da página
                        total_image_area += default_area
                        continue

                # Soma as áreas de todas as instâncias desta imagem
                for bbox in image_instances:
                    area = bbox.width * bbox.height
                    if area > 0:
                        total_image_area += area

            except Exception:
                # Em caso de erro, assume área conservadora
                default_area = min(page_area * 0.2, page_area * 0.2)
                total_image_area += default_area
                continue

        # Calcula a porcentagem, limitando a 100%
        coverage = min(total_image_area / page_area, 1.0) if page_area > 0 else 0
        return coverage


    def analyze_pdf(self, pdf_path: str) -> PDFResult:
        """
        Analisa um arquivo PDF e retorna informações completas

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            PDFInfo: Informações completas do PDF analisado

        Raises:
            PDFFileError: Se o arquivo não existe ou não pode ser lido
            PDFAnalysisError: Se ocorrer erro durante a análise
        """
        pdf_file = Path(pdf_path)
        self._validate_pdf_file(pdf_file)

        try:
            # Detecção básica do tipo
            basic_type = self._detect_basic_type(pdf_file)
            if basic_type == PDFType.IMAGE:
                return self._create_image_pdf_info(pdf_file)

            # Análise detalhada
            return self._perform_detailed_analysis(pdf_file)

        except Exception as e:
            logger.error(f"Erro durante análise do PDF {pdf_path}: {e}")
            raise PDFAnalysisException(f"Falha na análise do PDF: {e}") from e

    def extract_text(self, pdf_path: str) -> str:
        """
        Extrai texto de um PDF mantendo a estrutura

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            str: Texto extraído do PDF

        Raises:
            PDFFileError: Se o arquivo não existe ou não pode ser lido
        """
        pdf_file = Path(pdf_path)
        self._validate_pdf_file(pdf_file)

        try:
            pdf_doc = fitz.open(str(pdf_file))
            full_text = ""

            for page_num in range(len(pdf_doc)):
                page = pdf_doc.load_page(page_num)
                text_blocks = page.get_text("blocks")

                page_text = ""
                for block in text_blocks:
                    if len(block) > 4:  # Verifica se o bloco tem texto
                        page_text += block[4]

                full_text += f"\n{page_text}"

            pdf_doc.close()
            return full_text.strip()

        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {e}")
            raise PDFAnalysisException(f"Falha na extração de texto: {e}") from e

    def get_pdf_type(self, pdf_path: str) -> PDFType:
        """
        Retorna apenas o tipo do PDF (método mais rápido)

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            PDFType: Tipo do PDF analisado
        """
        try:
            pdf_info = self.analyze_pdf(pdf_path)
            return pdf_info.pdf_type
        except Exception as e:
            logger.error(f"Erro ao determinar tipo do PDF: {e}")
            return PDFType.UNKNOWN

    def _validate_pdf_file(self, pdf_file: Path) -> None:
        """Valida se o arquivo PDF existe e pode ser lido"""
        if not pdf_file.exists():
            raise PDFFileException(f"Arquivo PDF não encontrado: {pdf_file}")

        if not pdf_file.is_file():
            raise PDFFileException(f"Caminho não é um arquivo: {pdf_file}")

        if pdf_file.suffix.lower() != '.pdf':
            raise PDFFileException(f"Arquivo não é um PDF: {pdf_file}")

    def _detect_basic_type(self, pdf_path: Path) -> PDFType:
        """
        Detecta se o PDF contém fontes (texto extraível)

        Args:
            pdf_path: Caminho para o arquivo PDF

        Returns:
            PDFType: IMAGE se não tem fontes, caso contrário precisa análise mais detalhada
        """
        try:
            with open(pdf_path, 'rb') as f:
                for page in PDFPage.get_pages(f):
                    if "Font" in page.resources.keys():
                        return PDFType.UNKNOWN  # Precisa de análise mais detalhada

            return PDFType.IMAGE

        except Exception as e:
            logger.error(f"Erro na detecção básica do tipo de PDF: {e}")
            return PDFType.UNKNOWN

    def _create_image_pdf_info(self, pdf_file: Path) -> PDFResult:
        """Cria PDFInfo para PDF baseado em imagem"""
        try:
            doc = fitz.open(str(pdf_file))
            total_pages = len(doc)
            doc.close()

            return PDFResult(
                pdf_type=PDFType.IMAGE,
                total_pages=total_pages,
                text_pages=0,
                image_pages=total_pages,
                mixed_pages=0,
                total_text_length=0,
                total_image_coverage=1.0,
                pages_analysis=[],
                pdf_text=""
            )
        except Exception as e:
            logger.error(f"Erro ao analisar PDF de imagem: {e}")
            return self._create_unknown_pdf_info()

    def _perform_detailed_analysis(self, pdf_file: Path) -> PDFResult:
        """Realiza análise detalhada do PDF"""
        try:
            doc = fitz.open(str(pdf_file))

            analysis_data = {
                'total_pages': len(doc),
                'text_pages': 0,
                'image_pages': 0,
                'mixed_pages': 0,
                'total_text_length': 0,
                'total_image_coverage': 0.0,
                'pages_analysis': []
            }

            # Analisa cada página
            for page_num in range(analysis_data['total_pages']):
                page_analysis = self._analyze_single_page(doc[page_num], page_num)
                analysis_data['pages_analysis'].append(page_analysis)

                # Atualiza contadores
                self._update_analysis_counters(analysis_data, page_analysis)

            doc.close()

            # Extrai texto completo
            pdf_text = self.extract_text(pdf_file)

            # Determina tipo final do PDF
            pdf_type = self._determine_final_pdf_type(analysis_data)

            return PDFResult(
                pdf_type=pdf_type,
                total_pages=analysis_data['total_pages'],
                text_pages=analysis_data['text_pages'],
                image_pages=analysis_data['image_pages'],
                mixed_pages=analysis_data['mixed_pages'],
                total_text_length=analysis_data['total_text_length'],
                total_image_coverage=round(analysis_data['total_image_coverage'], 3),
                pages_analysis=analysis_data['pages_analysis'],
                pdf_text=pdf_text
            )

        except Exception as e:
            logger.error(f"Erro na análise detalhada: {e}")
            return self._create_unknown_pdf_info()

    def _analyze_single_page(self, page: fitz.Page, page_num: int) -> PDFPageResult:
        """Analisa uma única página do PDF"""
        try:
            page_area = page.rect.width * page.rect.height

            # Extrai e limpa texto
            text = page.get_text().strip()
            clean_text = re.sub(r'\s+', ' ', text)

            # Calcula cobertura de imagem
            image_coverage = self._calculate_image_coverage(page, page_area)

            # Conta imagens
            image_list = page.get_images()

            # Análise da página
            has_meaningful_text = len(clean_text) > self.config.min_text_threshold
            has_high_image_coverage = image_coverage > self.config.max_image_coverage
            has_images = len(image_list) > 0

            # Determina tipo da página
            page_type = self._determine_page_type(
                has_meaningful_text, has_high_image_coverage, has_images
            )

            return PDFPageResult(
                page_number=page_num + 1,
                page_type=page_type,
                text_length=len(clean_text),
                image_count=len(image_list),
                image_coverage=round(image_coverage, 3),
                has_meaningful_text=has_meaningful_text,
                has_high_image_coverage=has_high_image_coverage
            )

        except Exception as e:
            logger.warning(f"Erro ao analisar página {page_num + 1}: {e}")
            return PDFPageResult(
                page_number=page_num + 1,
                page_type=PDFPageType.UNKNOWN,
                text_length=0,
                image_count=0,
                image_coverage=0.0,
                has_meaningful_text=False,
                has_high_image_coverage=False
            )

    def _calculate_image_coverage(self, page: fitz.Page, page_area: float) -> float:
        """
        Calcula a porcentagem da página ocupada por imagens

        Args:
            page: Objeto da página do PyMuPDF
            page_area: Área total da página

        Returns:
            float: Porcentagem de cobertura de imagem (0.0 a 1.0)
        """
        try:
            image_list = page.get_images()
            if not image_list:
                return 0.0

            total_image_area = 0.0

            for img in image_list:
                image_area = self._calculate_single_image_area(page, img, page_area)
                total_image_area += image_area

            # Calcula a porcentagem, limitando a 100%
            coverage = min(total_image_area / page_area, 1.0) if page_area > 0 else 0.0
            return coverage

        except Exception as e:
            logger.warning(f"Erro ao calcular cobertura de imagem: {e}")
            return self.config.default_image_area_ratio

    def _calculate_single_image_area(self, page: fitz.Page, img: tuple, page_area: float) -> float:
        """Calcula a área de uma única imagem"""
        try:
            # Método 1: Usar get_image_bbox se disponível
            bbox = self._get_image_bbox_method1(page, img)
            if bbox:
                return bbox.width * bbox.height

            # Método 2: Procurar através do conteúdo da página
            bbox = self._get_image_bbox_method2(page)
            if bbox:
                return bbox.width * bbox.height

            # Método 3: Estimativa baseada em dimensões
            area = self._estimate_image_area(page, img, page_area)
            return area

        except Exception as e:
            logger.debug(f"Erro ao calcular área da imagem: {e}")
            return page_area * self.config.default_image_area_ratio

    def _get_image_bbox_method1(self, page: fitz.Page, img: tuple) -> Optional[fitz.Rect]:
        """Método 1: Usar get_image_bbox"""
        try:
            bbox = page.get_image_bbox(img)
            if bbox and bbox != fitz.Rect():
                return bbox
        except Exception:
            pass
        return None

    def _get_image_bbox_method2(self, page: fitz.Page) -> Optional[fitz.Rect]:
        """Método 2: Procurar através do conteúdo da página"""
        try:
            page_dict = page.get_text("dict")
            if 'blocks' in page_dict:
                for block in page_dict['blocks']:
                    if block.get('type') == 1:  # Tipo 1 = bloco de imagem
                        return fitz.Rect(block['bbox'])
        except Exception:
            pass
        return None

    def _estimate_image_area(self, page: fitz.Page, img: tuple, page_area: float) -> float:
        """Método 3: Estimativa baseada em dimensões"""
        try:
            xref = img[0]
            pix = fitz.Pixmap(page.parent, xref)

            if not pix:
                return page_area * self.config.default_image_area_ratio

            # Calcula escala aproximada
            scale_x = min(page.rect.width * 0.8, pix.width) / pix.width
            scale_y = min(page.rect.height * 0.8, pix.height) / pix.height
            scale = min(scale_x, scale_y)

            estimated_area = pix.width * pix.height * scale * scale
            pix = None  # Libera memória

            return min(estimated_area, page_area * self.config.max_image_area_ratio)

        except Exception:
            return page_area * self.config.default_image_area_ratio

    def _determine_page_type(self, has_meaningful_text: bool,
                             has_high_image_coverage: bool, has_images: bool) -> PDFPageType:
        """Determina o tipo de uma página baseado em suas características"""
        if has_meaningful_text and not has_high_image_coverage:
            return PDFPageType.TEXT
        elif has_high_image_coverage or (has_images and not has_meaningful_text):
            return PDFPageType.IMAGE
        elif has_meaningful_text and has_images:
            return PDFPageType.MIXED
        else:
            return PDFPageType.UNKNOWN

    def _update_analysis_counters(self, analysis_data: Dict, page_analysis: PDFPageResult) -> None:
        """Atualiza contadores da análise"""
        analysis_data['total_text_length'] += page_analysis.text_length
        analysis_data['total_image_coverage'] += page_analysis.image_coverage

        if page_analysis.page_type == PDFPageType.TEXT:
            analysis_data['text_pages'] += 1
        elif page_analysis.page_type == PDFPageType.IMAGE:
            analysis_data['image_pages'] += 1
        elif page_analysis.page_type == PDFPageType.MIXED:
            analysis_data['mixed_pages'] += 1

    def _determine_final_pdf_type(self, analysis_data: Dict) -> PDFType:
        """Determina o tipo final do PDF baseado na análise das páginas"""
        text_pages = analysis_data['text_pages']
        image_pages = analysis_data['image_pages']
        mixed_pages = analysis_data['mixed_pages']

        # Se tem páginas mistas, é um PDF misto
        if mixed_pages > 0:
            return PDFType.MIXED

        # Se predomina texto
        if text_pages > image_pages:
            return PDFType.TEXT

        # Se predomina imagem
        if image_pages > text_pages:
            return PDFType.IMAGE

        # Se empate ou nenhum tipo identificado
        return PDFType.UNKNOWN

    def _create_unknown_pdf_info(self) -> PDFResult:
        """Cria PDFInfo para PDF de tipo desconhecido"""
        return PDFResult(
            pdf_type=PDFType.UNKNOWN,
            total_pages=0,
            text_pages=0,
            image_pages=0,
            mixed_pages=0,
            total_text_length=0,
            total_image_coverage=0.0,
            pages_analysis=[],
            pdf_text=""
        )


# Exemplo de uso
if __name__ == "__main__":
    # Configuração customizada (opcional)
    config = PDFConfig(
        min_text_threshold=30,
        max_image_coverage=0.7
    )

    # Cria o service
    pdf_service = PDFService(config)

    try:
        # Analisa um PDF completo
        pdf_info = pdf_service.analyze_pdf("../../data/docs-test/CarteiraHabilitacao_Bruno.pdf")

        print(f"Tipo do PDF: {pdf_info.pdf_type.value}")
        print(f"Total de páginas: {pdf_info.total_pages}")
        print(f"Páginas de texto: {pdf_info.text_pages}")
        print(f"Páginas de imagem: {pdf_info.image_pages}")
        print(f"Páginas mistas: {pdf_info.mixed_pages}")
        print(f"Cobertura total de imagem: {pdf_info.total_image_coverage}")

        # Ou apenas extrair texto
        texto = pdf_service.extract_text("../../data/docs-test/CarteiraHabilitacao_Bruno.pdf")
        print(f"Texto extraído: {texto[:100]}...")

        # Ou apenas verificar o tipo
        tipo = pdf_service.get_pdf_type("../../data/docs-test/CarteiraHabilitacao_Bruno.pdf")
        print(f"Tipo: {tipo.value}")

    except (PDFFileException, PDFAnalysisException) as e:
        print(f"Erro: {e}")