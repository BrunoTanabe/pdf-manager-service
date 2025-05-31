from dataclasses import dataclass


@dataclass
class PDFConfig:
    """Configurações para análise de PDF."""

    min_text_threshold: int = 50
    min_text_ratio: float = 0.1
    max_image_coverage: float = 0.6
    max_default_image_area_ratio: float = 0.3
    image_scale_factor: float = 0.8
