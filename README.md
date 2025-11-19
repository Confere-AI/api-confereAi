# confereAi API

Este repositório contém a API do Confere-AI (desenvolvida com FastAPI) e os arquivos necessários para executar o sistema em containers Docker.

Visão geral
- Backend: pasta `app/` (FastAPI)
- Banco de dados: PostgreSQL (container)
- Migrações: Alembic

----

Requisitos
- Docker Desktop (Windows) com Compose habilitado
- PowerShell (no Windows) ou outro terminal
- (Opcional) Python 3.11+ para rodar localmente sem Docker

----

Preparar o ambiente
1. Copie o arquivo de exemplo de variáveis de ambiente para `.env` e ajuste conforme necessário:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env # ajuste valores se necessário
```

2. Verifique que o arquivo `.env` não foi adicionado ao repositório (ele já consta em `.gitignore`):

```powershell
git status --porcelain
```

3. Confirme o valor de `DATABASE_URL` em `.env` (exemplo: `postgresql+asyncpg://confere:confere@db:5432/confere`).

----

Executando com Docker Compose (recomendado)
1. Levante todos os serviços (Postgres, backend e serviço de migração):

```powershell
docker compose up --build -d
```

2. Verifique o status dos containers:

```powershell
docker compose ps
```

3. Acompanhe os logs do backend:

```powershell
docker compose logs -f web
```

4. Acesse a API:
- URL base: `http://localhost:8000`
- Documentação (Swagger): `http://localhost:8000/docs`
- Endpoint de saúde: `http://localhost:8000/health`

5. Caso seja necessário aplicar migrações manualmente (o serviço `migrate` tenta aplicar automaticamente no startup):

```powershell
docker compose run --rm migrate
```

6. Parar os serviços (mantendo os dados do banco):

```powershell
docker compose down
```

7. Parar e remover volumes (apagar dados do banco):

```powershell
docker compose down -v
```

----

Executando localmente sem Docker (desenvolvimento)
1. Crie e ative um ambiente virtual (PowerShell):

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

2. Instale as dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Inicie o servidor em modo de desenvolvimento:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. Acesse `http://localhost:8000/docs` para testar os endpoints.

----

Testes
1. Instale as dependências (se não estiver usando Docker):

```powershell
python -m pip install -r requirements.txt
```

2. Execute os testes com `pytest`:

Local:
```powershell
pytest -q
```

Dentro do container web:
```powershell
docker compose exec web pytest -q
```

----

Migrações (Alembic)
O projeto já possui `alembic` configurado. Para criar e aplicar migrações:

- Criar uma revisão automática a partir dos modelos:

```powershell
alembic revision --autogenerate -m "descrição"
```

- Aplicar migrações localmente:

```powershell
alembic upgrade head
```

- Aplicar migrações no Docker:

```powershell
docker compose run --rm migrate
```

Observação: o serviço `migrate` utiliza o script `scripts/wait_for_db.py` para aguardar o banco antes de executar as migrations.

----

Verificação de saúde (healthcheck)
- A aplicação expõe `GET /health` retornando `{ "status": "ok" }`. Esse endpoint é utilizado pelo `docker-compose` para verificar a saúde do serviço.

----

Segurança e boas práticas
- Não comite arquivos com credenciais (o `.env` está listado em `.gitignore`). Para produção, use secrets (Docker secrets, Vault, etc.).
- Em produção, restrinja CORS (atualmente está `allow_origins=["*"]` para desenvolvimento).
- Use logging estruturado em vez de `print()` para mensagens de runtime (substituições já aplicadas em alguns scripts).

----

Resolução de problemas (rápido)
- Se o `docker compose up` falhar no build por dependências nativas (por exemplo `asyncpg`), tente rebuild sem cache:

```powershell
docker compose build --no-cache web
```

- Se as migrations falharem por timeout de conexão, aumente `WAIT_TIMEOUT` ou execute:

```powershell
docker compose run --rm migrate
```

----

Se desejar, posso adaptar estas instruções para seu CI/CD (GitHub Actions, GitLab CI etc.).
