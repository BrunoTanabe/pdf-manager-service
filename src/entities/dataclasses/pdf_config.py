from dataclasses import dataclass

@dataclass
class PDFConfig:
    """Configurações para análise de PDF"""
    min_text_threshold: int = 50
    min_text_ratio: float = 0.1
    max_image_coverage: float = 0.6
    default_image_area_ratio: float = 0.2
    max_image_area_ratio: float = 0.3