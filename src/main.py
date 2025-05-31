import logging

from src.boundaries.pdf_service import PDFService
from src.controls.pdf_exception import PDFAnalysisException, PDFExtractionException
from src.entities.dataclasses.pdf_config import PDFConfig

# Exemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO)

    # Criar configuração personalizada
    config = PDFConfig(min_text_threshold=100, max_image_coverage=0.7)

    # Inicializar serviço
    pdf_service = PDFService(config)

    # Exemplo de uso
    try:
        pdf_file = "../data/docs-test/ComprovantedeVacinacao_Bruno.pdf"

        # Detectar tipo do PDF
        pdf_type = pdf_service.detect_pdf_type(pdf_file)
        print(f"Tipo do PDF: {pdf_type.value}")

        # Análise completa
        analysis = pdf_service.analyze_pdf(pdf_file)
        print(f"Total de páginas: {analysis.total_pages}")
        print(f"Páginas de texto: {analysis.text_pages}")
        print(f"Páginas de imagem: {analysis.image_pages}")
        print(f"Comprimento total do texto: {analysis.total_text_length} caracteres")
        print(f"Cobertura média de imagens: {analysis.average_image_coverage}")
        for page_analysis in analysis.pages_analysis:
            print(
                f"Página {page_analysis.page_number}: Tipo={page_analysis.type.value}, "
                f"Texto={page_analysis.text_length} caracteres, "
                f"Imagens={page_analysis.image_count}, "
                f"Cobertura de Imagem={page_analysis.image_coverage}"
            )
        print(f"Tipo geral do PDF: {analysis.pdf_type.value}")
        print(f"Total de páginas analisadas: {len(analysis.pages_analysis)}")

        # Extrair texto
        text = pdf_service.extract_pdf_text(pdf_file)
        print(f"Texto extraído: {len(text)} caracteres")

    except (
        PDFAnalysisException,
        PDFExtractionException,
        FileNotFoundError,
    ) as e:
        print(f"Erro: {e}")
