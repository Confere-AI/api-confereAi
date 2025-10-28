# API de Inferência (layout mínimo)

Este repositório contém um layout mínimo para um serviço de inferência baseado em FastAPI.

Estrutura

- `app/`
  - `main.py`: ponto de entrada do FastAPI
  - `controllers/`: endpoints REST (por exemplo, `inference_controller.py`)
  - `services/`: lógica de inferência e pré-processamento
  - `utils/`: utilitários como carregador de modelos
  - `models/`: coloque os artefatos treinados aqui (ex.: `model.pt`)
  - `tests/`: testes simples com pytest

Como começar

1. Crie um ambiente virtual e instale as dependências:

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Execute a aplicação localmente:

```pwsh
uvicorn app.main:app --reload
```

3. Execute os testes (requer `pytest` instalado):

```pwsh
pip install pytest
pytest -q
```

Próximos passos

- Substituir o `loader` e o `predictor` por lógica real de carregamento e inferência do modelo.
- Adicionar configuração de ambiente em `app/core`.
- Fortalecer o `Dockerfile` e adicionar integração contínua (CI).
