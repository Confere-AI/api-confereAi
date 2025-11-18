# confereAi API

Este repositório contém a API em FastAPI com PostgreSQL (asyncpg + SQLAlchemy) e migrações via Alembic.

Objetivo deste README
- Guia rápido e prático para executar, desenvolver e migrar o banco. Comandos prontos em PowerShell (Windows) e notas para Docker.

## Índice
- Resumo rápido
- Pré-requisitos
- Quick start — Docker (recomendado)
- Desenvolvimento com hot-reload
- Migrações (Alembic)
- Testes
- Executar localmente (venv)
- Acessar o banco (psql)
- Troubleshooting rápido
- Contribuindo (mínimo)
- CI e publicação (nota)

---

## Resumo rápido
- Levantar tudo (prod-like):

```powershell
docker compose up --build
```

- Levantar dev com hot-reload:

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## Pré-requisitos
- Docker e Docker Compose (recomendado).
- Python 3.11 (se for usar venv localmente).
- Copie `.env.example` para `.env` antes de rodar.

## Quick start — Docker (recomendado)
1. Clone o repositório e entre na pasta:

```powershell
git clone <repo-url>
cd api-confereAi
```

2. Copie variáveis de ambiente:

```powershell
cp .env.example .env
# editar .env conforme necessário
```

3. Suba os serviços (Postgres, web, migrate):

```powershell
docker compose up --build
# em background
docker compose up -d --build
```

4. A API ficará disponível em `http://localhost:8000`.

Observação: o serviço `migrate` já executa `alembic upgrade head` conforme `docker-compose.yml`.

## Desenvolvimento com hot-reload
Use `docker-compose.dev.yml` para montar o código e rodar `uvicorn` com reload:

```powershell
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

## Migrações (Alembic)
- Gerar migration (após alterar models):

```powershell
docker compose run --rm web alembic revision --autogenerate -m "Descrição da mudança"
```

- Revisar o arquivo em `alembic/versions/` e, se OK, aplicar:

```powershell
docker compose run --rm migrate
# ou
docker compose run --rm web alembic upgrade head
```

Fluxo mínimo recomendado ao alterar schema:
1) Atualizar `app/models/*.py`.
2) `alembic revision --autogenerate`.
3) Revisar e ajustar a migration.
4) `alembic upgrade head`.
5) Rodar testes.

## Testes
- Dentro do container (recomendado):

```powershell
docker compose run --rm web sh -c "pip install pytest && pytest -q"
```

- Local (venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pytest
pytest -q
```

## Executar localmente (venv)
- Use venv apenas para dev rápido. Docker é recomendado para evitar problemas de compilação (especialmente no Windows com `asyncpg`).

## Acessar o banco (psql)

```powershell
docker compose exec db psql -U confere -d confere
```

Para scripts de inicialização automática, coloque-os em `/docker-entrypoint-initdb.d/`.

## Troubleshooting rápido
- `asyncpg` falha no Windows: instale o Visual C++ Build Tools ou use Docker para evitar compilação local.
- `alembic` não encontra `app`: o `Dockerfile` já define `ENV PYTHONPATH=/app` para resolver esse problema.
- Remover containers e volumes (apaga dados):

```powershell
docker compose down -v
```

## Contribuindo (mínimo)
- Ao alterar schema:
  1. Atualize `app/models`.
  2. Gere migration: `alembic revision --autogenerate`.
  3. Revise e commite a migration em `alembic/versions/`.
  4. Aplique em CI/ambiente local e rode testes.

- Recomendo adicionar `CONTRIBUTING.md` e `pre-commit` (black/ruff) — posso criar isso se desejar.

## CI e publicação (nota)
- Existe um workflow de CI em `.github/workflows/ci.yml` que roda `pytest` e builda a imagem.
- Para publicar a imagem no GHCR/Docker Hub é necessário configurar secrets no repositório; eu posso adaptar o workflow para `build-and-push` quando você confirmar o registry e fornecer os secrets.

---

Se quiser que eu faça agora alguma ação (ex.: criar `CONTRIBUTING.md`, adicionar `pre-commit` ou configurar publicação no GHCR), diga qual e eu executo.


