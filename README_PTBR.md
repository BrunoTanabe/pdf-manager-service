# PDF Manager Service 📄🔍

##### 🇺🇸 [READ THIS README IN ENGLISH!](README.md)

Simplifique e automatize o processamento de documentos PDF com inteligência e modularidade! 🚀 O **PDF Manager Service** é um serviço extensível desenvolvido em Python que oferece detecção automática de tipos de conteúdo, extração inteligente de texto e análise estrutural completa de arquivos PDF. Com uma arquitetura modular bem definida e configurações personalizáveis, esta solução foi criada para atender necessidades específicas de um projeto, mas é flexível o suficiente para servir como base para fluxos de trabalho escaláveis de processamento de PDFs.

---

## Sumário 📋

[PDF Manager Service 📄🔍](#pdf-manager-service-)  
  [Sumário 📋](#sumário-)  
  [1. Descrição 📖](#1-descrição-)  
  [2. Objetivos 🎯](#2-objetivos-)  
  [3. Principais Funcionalidades ⚙️](#3-principais-funcionalidades-️)  
  [4. Principais Tecnologias Utilizadas 💻](#4-principais-tecnologias-utilizadas-)  
  [5. Estrutura do Projeto 📁](#5-estrutura-do-projeto-)  
  [6. Arquitetura 🏗️](#6-arquitetura-️)  
  [7. Requisitos 🔧](#7-requisitos-)  
  [8. Como Executar? 🏃‍♂️](#8-como-executar-️)  
  [9. Exemplos de Uso 💡](#9-exemplos-de-uso-)  
  [10. Configurações 🔧](#10-configurações-)  
  [11. Testes 🧪](#11-testes-)  
  [12. TODOs 🔮](#12-todos-)  
  [13. Licença 📄](#13-licença-)  
  [14. Como Contribuir? 🤝](#14-como-contribuir-)  
  [15. Autor e Contato 👤](#15-autor-e-contato-)  

---

## 1. Descrição 📖

Bem-vindo ao **PDF Manager Service**! Este é um serviço modular e extensível desenvolvido em Python para gerenciamento inteligente de arquivos PDF. O sistema oferece funcionalidades avançadas para detectar automaticamente se o conteúdo de um PDF é principalmente texto ou imagens, extrair texto de forma eficiente e realizar análises estruturais detalhadas página por página. Com uma arquitetura bem definida e configurações personalizáveis, o serviço é ideal tanto para necessidades específicas quanto para servir como fundação para workflows escaláveis de processamento de documentos.

---

## 2. Objetivos 🎯

- **Detecção Automática**: Identificar automaticamente se o conteúdo do PDF é principalmente texto ou imagens.
- **Extração Inteligente**: Extrair texto de PDFs de forma eficiente e precisa.
- **Análise Estrutural**: Fornecer análises detalhadas da estrutura do documento página por página.
- **Modularidade**: Oferecer uma arquitetura flexível e extensível para diferentes necessidades.
- **Configurabilidade**: Permitir personalização de parâmetros de análise conforme requisitos específicos.

---

## 3. Principais Funcionalidades ⚙️

- **Detecção de Tipo de PDF**: Classifica automaticamente PDFs como TEXT, IMAGE ou UNKNOWN.
- **Análise Página por Página**: Analisa cada página individualmente para detectar conteúdo e estrutura.
- **Extração de Texto**: Extrai texto completo de documentos PDF com alta precisão.
- **Análise de Cobertura de Imagens**: Calcula a cobertura de imagens em cada página.
- **Configurações Personalizáveis**: Permite ajustar thresholds e parâmetros de análise.
- **Tratamento de Exceções**: Sistema robusto de tratamento de erros específicos para PDFs.
- **Logging Integrado**: Sistema de logging configurável para monitoramento e debug.

---

## 4. Principais Tecnologias Utilizadas 💻

- **Linguagem**: Python 3.10+
- **Processamento de PDF**: PyMuPDF (Fitz) e pdfminer-six
- **Gerenciamento de Dependências**: uv (Astral)
- **Testes**: pytest
- **Formatação e Linting**: Ruff
- **Automação de Tarefas**: Taskipy

---

## 5. Estrutura do Projeto 📁

A estrutura do projeto segue uma arquitetura modular bem definida:

```
pdf-manager-service/
│
├── .venv/              # Ambiente virtual Python
├── data/               # Dados e arquivos de teste
├── notebook/           # Jupyter notebooks para análises
├── src/                # Código-fonte principal
│   ├── boundaries/     # Camada de interface/serviços
│   │   ├── pdf_service.py
│   │   ├── pdf_image_coverage.py
│   │   └── pdf_page_analyzer.py
│   ├── controls/       # Camada de controle/exceções
│   │   └── pdf_exception.py
│   ├── entities/       # Entidades e modelos de dados
│   │   ├── dataclasses/
│   │   │   ├── pdf_config.py
│   │   │   ├── pdf_analysis_result.py
│   │   │   └── pdf_page_analysis.py
│   │   └── enums/
│   │       ├── pdf_type.py
│   │       └── pdf_page_type.py
│   └── main.py         # Exemplo de uso
├── .gitignore          # Arquivos ignorados pelo Git
├── .python-version     # Versão do Python
├── pyproject.toml      # Configuração do projeto e dependências
├── README.md           # README em inglês
├── README_PTBR.md      # Este arquivo (Português)
├── requirements.txt    # Dependências principais (para pip)
├── requirements-dev.txt # Dependências de desenvolvimento (para pip)
├── uv.lock             # Lock file das dependências
├── LICENSE             # Licença do projeto
└── README.md           # Este arquivo
```

---

## 6. Arquitetura 🏗️

O projeto segue uma **Arquitetura Limpa** com separação clara de responsabilidades:

### Boundaries (Fronteiras)
- **PDFService**: Serviço principal que orquestra todas as funcionalidades
- **PDFImageCoverage**: Analisa a cobertura de imagens em páginas
- **PDFPageAnalyzer**: Analisa páginas individuais

### Controls (Controles)
- **PDFException**: Exceções específicas para tratamento de erros

### Entities (Entidades)
- **DataClasses**: Modelos de dados (PDFConfig, PDFAnalysisResult, PDFPageAnalysis)
- **Enums**: Tipos enumerados (PDFType, PDFPageType)

---

## 7. Requisitos 🔧

- **Python 3.10** ou superior
- **Gerenciador de Dependências** (escolha uma das opções):
  - **uv** (Astral) - ⭐ Recomendado
  - **pip** + venv (tradicional)
  - **poetry** 
  - **pipenv**

---

## 8. Como Executar? 🏃‍♂️

Escolha uma das opções abaixo para executar o projeto:

> **💡 Qual método escolher?**
> - **uv**: Mais rápido e moderno, recomendado para desenvolvimento
> - **pip + venv**: Tradicional, funciona em qualquer ambiente Python
> - **poetry**: Bom para projetos que já usam Poetry
> - **pipenv**: Alternativa ao Poetry, combina pip e virtualenv

### 8.1. Usando uv (Recomendado) ⭐

#### 8.1.1. Instalação do uv

```bash
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS e Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 8.1.2. Clonando e Executando

```bash
# Clonar repositório
git clone https://github.com/SeuUsuario/pdf-manager-service.git
cd pdf-manager-service

# Sincronizar dependências
uv sync

# Executar exemplo
uv run python src/main.py
```

#### 8.1.3. Comandos Úteis com uv

```bash
# Executar testes
uv run task test

# Verificar formatação
uv run task lint

# Corrigir formatação
uv run task format
```

### 8.2. Usando pip + venv (Tradicional) 🐍

#### 8.2.1. Clonando e Preparando Ambiente

```bash
# Clonar repositório
git clone https://github.com/SeuUsuario/pdf-manager-service.git
cd pdf-manager-service

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

#### 8.2.2. Instalando Dependências

```bash
# Opção 1: Instalar apenas dependências principais
pip install -r requirements.txt

# Opção 2: Instalar com dependências de desenvolvimento
pip install -r requirements-dev.txt

# Opção 3: Instalar manualmente
pip install pdfminer-six>=20250506 pymupdf>=1.26.0

# Opção 4: Instalar manualmente com dependências de desenvolvimento
pip install pdfminer-six>=20250506 pymupdf>=1.26.0 notebook>=7.4.3 pytest>=8.3.5 ruff>=0.11.11 taskipy>=1.14.1
```

#### 8.2.3. Executando

```bash
# Executar exemplo
python src/main.py

# Executar testes
pytest

# Verificar formatação
ruff check .
```

### 8.3. Usando Poetry 📝

#### 8.3.1. Instalação do Poetry

```bash
# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

# Linux/macOS
curl -sSL https://install.python-poetry.org | python3 -
```

#### 8.3.2. Configurando com Poetry

Primeiro, crie um arquivo `pyproject.toml` compatível com Poetry ou use o existente:

```bash
# Clonar repositório
git clone https://github.com/SeuUsuario/pdf-manager-service.git
cd pdf-manager-service

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell

# Executar exemplo
poetry run python src/main.py
```

#### 8.3.3. Comandos Úteis com Poetry

```bash
# Executar testes
poetry run pytest

# Verificar formatação
poetry run ruff check .

# Adicionar nova dependência
poetry add nome-do-pacote
```

### 8.4. Usando Pipenv 🧪

#### 8.4.1. Instalação do Pipenv

```bash
pip install pipenv
```

#### 8.4.2. Configurando com Pipenv

```bash
# Clonar repositório
git clone https://github.com/SeuUsuario/pdf-manager-service.git
cd pdf-manager-service

# Criar Pipfile (se não existir)
pipenv install pdfminer-six>=20250506 pymupdf>=1.26.0

# Instalar dependências de desenvolvimento
pipenv install --dev notebook>=7.4.3 pytest>=8.3.5 ruff>=0.11.11 taskipy>=1.14.1

# Ativar ambiente virtual
pipenv shell

# Executar exemplo
pipenv run python src/main.py
```

#### 8.4.3. Comandos Úteis com Pipenv

```bash
# Executar testes
pipenv run pytest

# Verificar formatação
pipenv run ruff check .

# Ver dependências
pipenv graph
```

### 8.5. Resumo de Comandos por Gerenciador

| Ação | uv | pip + venv | poetry | pipenv |
|------|----|-----------| -------|--------|
| **Instalar deps** | `uv sync` | `pip install -r requirements.txt` | `poetry install` | `pipenv install` |
| **Executar exemplo** | `uv run python src/main.py` | `python src/main.py` | `poetry run python src/main.py` | `pipenv run python src/main.py` |
| **Executar testes** | `uv run task test` | `pytest` | `poetry run pytest` | `pipenv run pytest` |
| **Verificar código** | `uv run task lint` | `ruff check .` | `poetry run ruff check .` | `pipenv run ruff check .` |

---

## 9. Exemplos de Uso 💡

### 9.1. Uso Básico

```python
from src.boundaries.pdf_service import PDFService
from src.entities.dataclasses.pdf_config import PDFConfig

# Criar configuração padrão
config = PDFConfig()

# Inicializar serviço
pdf_service = PDFService(config)

# Detectar tipo do PDF
pdf_type = pdf_service.detect_pdf_type("arquivo.pdf")
print(f"Tipo do PDF: {pdf_type.value}")

# Extrair texto
text = pdf_service.extract_pdf_text("arquivo.pdf")
print(f"Texto extraído: {len(text)} caracteres")
```

### 9.2. Análise Completa

```python
# Análise detalhada do PDF
analysis = pdf_service.analyze_pdf("arquivo.pdf")

print(f"Total de páginas: {analysis.total_pages}")
print(f"Páginas de texto: {analysis.text_pages}")
print(f"Páginas de imagem: {analysis.image_pages}")
print(f"Tipo geral: {analysis.pdf_type.value}")

# Análise por página
for page_analysis in analysis.pages_analysis:
    print(f"Página {page_analysis.page_number}: {page_analysis.type.value}")
```

### 9.3. Configuração Personalizada

```python
# Configuração personalizada
config = PDFConfig(
    min_text_threshold=100,
    max_image_coverage=0.7,
    min_text_ratio=0.15
)

pdf_service = PDFService(config)
```

---

## 10. Configurações 🔧

O serviço permite personalização através da classe `PDFConfig`:

```python
@dataclass
class PDFConfig:
    min_text_threshold: int = 50          # Mínimo de caracteres para considerar texto
    min_text_ratio: float = 0.1           # Razão mínima de texto
    max_image_coverage: float = 0.6       # Cobertura máxima de imagens
    max_default_image_area_ratio: float = 0.3  # Razão máxima de área de imagem
    image_scale_factor: float = 0.8       # Fator de escala para imagens
```

---

## 11. Testes 🧪

O projeto inclui testes automatizados com pytest:

```bash
# Executar todos os testes com coverage
uv run task test

# Executar testes específicos
uv run pytest tests/test_pdf_service.py

# Gerar relatório de coverage em HTML
uv run task post_test
```

Os relatórios de coverage são gerados na pasta `htmlcov/`.

---

## 12. TODOs 🔮

- **API REST**: Criar uma API REST com FastAPI para acesso via HTTP ⚡
- **Interface Web**: Desenvolver uma interface web para upload e análise de PDFs 🌐
- **Processamento em Lote**: Implementar processamento de múltiplos PDFs simultaneamente 📦
- **Cache Inteligente**: Sistema de cache para otimizar análises repetidas 🚀
- **Suporte a OCR**: Integração com OCR para PDFs escaneados 👁️
- **Métricas Avançadas**: Mais métricas de análise estrutural 📊
- **Containerização**: Dockerização da aplicação 🐳
- **CI/CD**: Pipeline de integração e deploy contínuo 🔄

---

## 13. Licença 📄

Este projeto está licenciado sob a Licença MIT. Para mais informações, leia o arquivo [LICENSE](LICENSE).

---

## 14. Como Contribuir? 🤝

Contribuições são muito bem-vindas! Siga os passos abaixo:

1. Faça um *fork* do repositório.
2. Crie uma branch para a feature:
   ```bash
   git checkout -b feature/nova-feature
   ```
3. Instale as dependências de desenvolvimento:
   ```bash
   uv sync
   ```
4. Faça suas alterações e teste:
   ```bash
   uv run task test
   uv run task lint
   ```
5. Faça o commit das alterações:
   ```bash
   git commit -m "feat: adiciona nova feature"
   ```
6. Faça o push para o seu repositório remoto:
   ```bash
   git push origin feature/nova-feature
   ```
7. Abra um Pull Request neste repositório.

---

## 15. Autor e Contato 👤

- **Nome**: Bruno Tanabe
- **Email**: [tanabebruno@gmail.com](mailto:tanabebruno@gmail.com)
- **LinkedIn**: [linkedin.com/in/tanabebruno](https://www.linkedin.com/in/tanabebruno/)
- **GitHub**: [github.com/brunotanabe](https://github.com/brunotanabe)
- **Medium**: [medium.com/@tanabebruno](https://medium.com/@tanabebruno)

---

**Desenvolvido com ❤️ e Python** 🐍 