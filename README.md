# PDF Manager Service 📄🔍

##### 🇧🇷 [LEIA ESTE README EM PORTUGUÊS!](README_PTBR.md)

Simplify and automate PDF document processing with intelligence and modularity! 🚀 The **PDF Manager Service** is an extensible service developed in Python that offers automatic content type detection, intelligent text extraction, and comprehensive structural analysis of PDF files. With a well-defined modular architecture and customizable configurations, this solution was created to meet specific project needs, but is flexible enough to serve as a foundation for scalable PDF processing workflows.

---

## Table of Contents 📋

[PDF Manager Service 📄🔍](#pdf-manager-service-)  
  [Table of Contents 📋](#table-of-contents-)  
  [1. Description 📖](#1-description-)  
  [2. Objectives 🎯](#2-objectives-)  
  [3. Main Features ⚙️](#3-main-features-️)  
  [4. Main Technologies Used 💻](#4-main-technologies-used-)  
  [5. Project Structure 📁](#5-project-structure-)  
  [6. Architecture 🏗️](#6-architecture-️)  
  [7. Requirements 🔧](#7-requirements-)  
  [8. How to Run? 🏃‍♂️](#8-how-to-run-️)  
  [9. Usage Examples 💡](#9-usage-examples-)  
  [10. Configuration 🔧](#10-configuration-)  
  [11. Testing 🧪](#11-testing-)  
  [12. TODOs 🔮](#12-todos-)  
  [13. License 📄](#13-license-)  
  [14. How to Contribute? 🤝](#14-how-to-contribute-)  
  [15. Author and Contact 👤](#15-author-and-contact-)  

---

## 1. Description 📖

Welcome to the **PDF Manager Service**! This is a modular and extensible service developed in Python for intelligent PDF file management. The system offers advanced features to automatically detect whether PDF content is primarily text or images, extract text efficiently, and perform detailed structural analysis page by page. With a well-defined architecture and customizable configurations, the service is ideal both for specific needs and to serve as a foundation for scalable document processing workflows.

---

## 2. Objectives 🎯

- **Automatic Detection**: Automatically identify whether PDF content is primarily text or images.
- **Intelligent Extraction**: Extract text from PDFs efficiently and accurately.
- **Structural Analysis**: Provide detailed analysis of document structure page by page.
- **Modularity**: Offer a flexible and extensible architecture for different needs.
- **Configurability**: Allow customization of analysis parameters according to specific requirements.

---

## 3. Main Features ⚙️

- **PDF Type Detection**: Automatically classifies PDFs as TEXT, IMAGE, or UNKNOWN.
- **Page-by-Page Analysis**: Analyzes each page individually to detect content and structure.
- **Text Extraction**: Extracts complete text from PDF documents with high precision.
- **Image Coverage Analysis**: Calculates image coverage on each page.
- **Customizable Settings**: Allows adjustment of thresholds and analysis parameters.
- **Exception Handling**: Robust system for handling PDF-specific errors.
- **Integrated Logging**: Configurable logging system for monitoring and debugging.

---

## 4. Main Technologies Used 💻

- **Language**: Python 3.10+
- **PDF Processing**: PyMuPDF (Fitz) and pdfminer-six
- **Dependency Management**: uv (Astral)
- **Testing**: pytest
- **Formatting and Linting**: Ruff
- **Task Automation**: Taskipy

---

## 5. Project Structure 📁

The project structure follows a well-defined modular architecture:

```
pdf-manager-service/
│
├── .venv/              # Python virtual environment
├── data/               # Data and test files
├── notebook/           # Jupyter notebooks for analysis
├── src/                # Main source code
│   ├── boundaries/     # Interface/services layer
│   │   ├── pdf_service.py
│   │   ├── pdf_image_coverage.py
│   │   └── pdf_page_analyzer.py
│   ├── controls/       # Control/exceptions layer
│   │   └── pdf_exception.py
│   ├── entities/       # Entities and data models
│   │   ├── dataclasses/
│   │   │   ├── pdf_config.py
│   │   │   ├── pdf_analysis_result.py
│   │   │   └── pdf_page_analysis.py
│   │   └── enums/
│   │       ├── pdf_type.py
│   │       └── pdf_page_type.py
│   └── main.py         # Usage example
├── .gitignore          # Files ignored by Git
├── .python-version     # Python version
├── pyproject.toml      # Project configuration and dependencies
├── README.md           # This file (English)
├── README_PTBR.md      # README in Portuguese
├── requirements.txt    # Main dependencies (for pip)
├── requirements-dev.txt # Development dependencies (for pip)
├── uv.lock             # Dependencies lock file
├── LICENSE             # Project license
└── README.md           # This file
```

---

## 6. Architecture 🏗️

The project follows **Clean Architecture** with clear separation of responsibilities:

### Boundaries
- **PDFService**: Main service that orchestrates all functionalities
- **PDFImageCoverage**: Analyzes image coverage on pages
- **PDFPageAnalyzer**: Analyzes individual pages

### Controls
- **PDFException**: Specific exceptions for error handling

### Entities
- **DataClasses**: Data models (PDFConfig, PDFAnalysisResult, PDFPageAnalysis)
- **Enums**: Enumerated types (PDFType, PDFPageType)

---

## 7. Requirements 🔧

- **Python 3.10** or higher
- **Dependency Manager** (choose one of the options):
  - **uv** (Astral) - ⭐ Recommended
  - **pip** + venv (traditional)
  - **poetry** 
  - **pipenv**

---

## 8. How to Run? 🏃‍♂️

Choose one of the options below to run the project:

> **💡 Which method to choose?**
> - **uv**: Faster and modern, recommended for development
> - **pip + venv**: Traditional, works in any Python environment
> - **poetry**: Good for projects already using Poetry
> - **pipenv**: Alternative to Poetry, combines pip and virtualenv

### 8.1. Using uv (Recommended) ⭐

#### 8.1.1. Installing uv

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 8.1.2. Cloning and Running

```bash
# Clone repository
git clone https://github.com/YourUser/pdf-manager-service.git
cd pdf-manager-service

# Sync dependencies
uv sync

# Run example
uv run python src/main.py
```

#### 8.1.3. Useful Commands with uv

```bash
# Run tests
uv run task test

# Check formatting
uv run task lint

# Fix formatting
uv run task format
```

### 8.2. Using pip + venv (Traditional) 🐍

#### 8.2.1. Cloning and Preparing Environment

```bash
# Clone repository
git clone https://github.com/YourUser/pdf-manager-service.git
cd pdf-manager-service

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

#### 8.2.2. Installing Dependencies

```bash
# Option 1: Install only main dependencies
pip install -r requirements.txt

# Option 2: Install with development dependencies
pip install -r requirements-dev.txt

# Option 3: Install manually
pip install pdfminer-six>=20250506 pymupdf>=1.26.0

# Option 4: Install manually with development dependencies
pip install pdfminer-six>=20250506 pymupdf>=1.26.0 notebook>=7.4.3 pytest>=8.3.5 ruff>=0.11.11 taskipy>=1.14.1
```

#### 8.2.3. Running

```bash
# Run example
python src/main.py

# Run tests
pytest

# Check formatting
ruff check .
```

### 8.3. Using Poetry 📝

#### 8.3.1. Installing Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -
```

#### 8.3.2. Setting up with Poetry

First, create a Poetry-compatible `pyproject.toml` file or use the existing one:

```bash
# Clone repository
git clone https://github.com/YourUser/pdf-manager-service.git
cd pdf-manager-service

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run example
poetry run python src/main.py
```

#### 8.3.3. Useful Commands with Poetry

```bash
# Run tests
poetry run pytest

# Check formatting
poetry run ruff check .

# Add new dependency
poetry add package-name
```

### 8.4. Using Pipenv 🧪

#### 8.4.1. Installing Pipenv

```bash
pip install pipenv
```

#### 8.4.2. Setting up with Pipenv

```bash
# Clone repository
git clone https://github.com/YourUser/pdf-manager-service.git
cd pdf-manager-service

# Create Pipfile (if it doesn't exist)
pipenv install pdfminer-six>=20250506 pymupdf>=1.26.0

# Install development dependencies
pipenv install --dev notebook>=7.4.3 pytest>=8.3.5 ruff>=0.11.11 taskipy>=1.14.1

# Activate virtual environment
pipenv shell

# Run example
pipenv run python src/main.py
```

#### 8.4.3. Useful Commands with Pipenv

```bash
# Run tests
pipenv run pytest

# Check formatting
pipenv run ruff check .

# View dependencies
pipenv graph
```

### 8.5. Command Summary by Manager

| Action | uv | pip + venv | poetry | pipenv |
|--------|----|-----------| -------|--------|
| **Install deps** | `uv sync` | `pip install -r requirements.txt` | `poetry install` | `pipenv install` |
| **Run example** | `uv run python src/main.py` | `python src/main.py` | `poetry run python src/main.py` | `pipenv run python src/main.py` |
| **Run tests** | `uv run task test` | `pytest` | `poetry run pytest` | `pipenv run pytest` |
| **Check code** | `uv run task lint` | `ruff check .` | `poetry run ruff check .` | `pipenv run ruff check .` |

---

## 9. Usage Examples 💡

### 9.1. Basic Usage

```python
from src.boundaries.pdf_service import PDFService
from src.entities.dataclasses.pdf_config import PDFConfig

# Create default configuration
config = PDFConfig()

# Initialize service
pdf_service = PDFService(config)

# Detect PDF type
pdf_type = pdf_service.detect_pdf_type("file.pdf")
print(f"PDF Type: {pdf_type.value}")

# Extract text
text = pdf_service.extract_pdf_text("file.pdf")
print(f"Extracted text: {len(text)} characters")
```

### 9.2. Complete Analysis

```python
# Detailed PDF analysis
analysis = pdf_service.analyze_pdf("file.pdf")

print(f"Total pages: {analysis.total_pages}")
print(f"Text pages: {analysis.text_pages}")
print(f"Image pages: {analysis.image_pages}")
print(f"General type: {analysis.pdf_type.value}")

# Page-by-page analysis
for page_analysis in analysis.pages_analysis:
    print(f"Page {page_analysis.page_number}: {page_analysis.type.value}")
```

### 9.3. Custom Configuration

```python
# Custom configuration
config = PDFConfig(
    min_text_threshold=100,
    max_image_coverage=0.7,
    min_text_ratio=0.15
)

pdf_service = PDFService(config)
```

---

## 10. Configuration 🔧

The service allows customization through the `PDFConfig` class:

```python
@dataclass
class PDFConfig:
    min_text_threshold: int = 50          # Minimum characters to consider text
    min_text_ratio: float = 0.1           # Minimum text ratio
    max_image_coverage: float = 0.6       # Maximum image coverage
    max_default_image_area_ratio: float = 0.3  # Maximum image area ratio
    image_scale_factor: float = 0.8       # Image scale factor
```

---

## 11. Testing 🧪

The project includes automated tests with pytest:

```bash
# Run all tests with coverage
uv run task test

# Run specific tests
uv run pytest tests/test_pdf_service.py

# Generate HTML coverage report
uv run task post_test
```

Coverage reports are generated in the `htmlcov/` folder.

---

## 12. TODOs 🔮

- **REST API**: Create a REST API with FastAPI for HTTP access ⚡
- **Web Interface**: Develop a web interface for PDF upload and analysis 🌐
- **Batch Processing**: Implement simultaneous processing of multiple PDFs 📦
- **Smart Cache**: Cache system to optimize repeated analyses 🚀
- **OCR Support**: Integration with OCR for scanned PDFs 👁️
- **Advanced Metrics**: More structural analysis metrics 📊
- **Containerization**: Docker containerization of the application 🐳
- **CI/CD**: Continuous integration and deployment pipeline 🔄

---

## 13. License 📄

This project is licensed under the MIT License. For more information, read the [LICENSE](LICENSE) file.

---

## 14. How to Contribute? 🤝

Contributions are very welcome! Follow the steps below:

1. Fork the repository.
2. Create a branch for the feature:
   ```bash
   git checkout -b feature/new-feature
   ```
3. Install development dependencies:
   ```bash
   uv sync
   ```
4. Make your changes and test:
   ```bash
   uv run task test
   uv run task lint
   ```
5. Commit your changes:
   ```bash
   git commit -m "feat: add new feature"
   ```
6. Push to your remote repository:
   ```bash
   git push origin feature/new-feature
   ```
7. Open a Pull Request in this repository.

---

## 15. Author and Contact 👤

- **Name**: Bruno Tanabe
- **Email**: [tanabebruno@gmail.com](mailto:tanabebruno@gmail.com)
- **LinkedIn**: [linkedin.com/in/tanabebruno](https://www.linkedin.com/in/tanabebruno/)
- **GitHub**: [github.com/brunotanabe](https://github.com/brunotanabe)
- **Medium**: [medium.com/@tanabebruno](https://medium.com/@tanabebruno)

---

**Developed with ❤️ and Python** 🐍
