class PDFException(Exception):
    """Exceção base para todas as operações relacionadas a PDF."""

    def __init__(
        self, message: str, original_exception: Exception = None, file_path: str = None
    ):
        self.message = message
        self.original_exception = original_exception
        self.file_path = file_path

        # Construir mensagem detalhada
        detailed_message = message
        if file_path:
            detailed_message += f" [Arquivo: {file_path}]"
        if original_exception:
            detailed_message += f" [Causa: {str(original_exception)}]"

        super().__init__(detailed_message)


class PDFAnalysisException(PDFException):
    """Exceção para erros na análise de estrutura e conteúdo de PDF."""

    def __init__(
        self,
        message: str = "Erro na análise do PDF",
        original_exception: Exception = None,
        file_path: str = None,
        page_number: int = None,
    ):
        self.page_number = page_number

        # Adicionar informação sobre a página à mensagem
        if page_number is not None:
            message += f" (na página {page_number})"

        super().__init__(message, original_exception, file_path)


class PDFExtractionException(PDFException):
    """Exceção para erros na extração de texto e conteúdo."""

    def __init__(
        self,
        message: str = "Erro na extração de conteúdo do PDF",
        original_exception: Exception = None,
        file_path: str = None,
        page_number: int = None,
    ):
        self.page_number = page_number

        # Adicionar informação sobre a página à mensagem
        if page_number is not None:
            message += f" (na página {page_number})"

        super().__init__(message, original_exception, file_path)
