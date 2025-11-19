# confereAi API

Este reposit�rio cont�m a API do Confere-AI (desenvolvida com FastAPI) e os arquivos necess�rios para executar o sistema em containers Docker.

Vis�o geral
- Backend: pasta `app/` (FastAPI)
- Banco de dados: PostgreSQL (container)
- Migra��es: Alembic

----

Requisitos
- Docker Desktop (Windows) com Compose habilitado
- PowerShell (no Windows) ou outro terminal
- (Opcional) Python 3.11+ para rodar localmente sem Docker

----

Preparar o ambiente
1. Copie o arquivo de exemplo de vari�veis de ambiente para `.env` e ajuste conforme necess�rio:

```powershell
Copy-Item .\.env.example .\.env
notepad .\.env # ajuste valores se necess�rio
```

2. Verifique que o arquivo `.env` n�o foi adicionado ao reposit�rio (ele j� consta em `.gitignore`):

```powershell
git status --porcelain
```

3. Confirme o valor de `DATABASE_URL` em `.env` (exemplo: `postgresql+asyncpg://confere:confere@db:5432/confere`).

----

Executando com Docker Compose (recomendado)
1. Levante todos os servi�os (Postgres, backend e servi�o de migra��o):

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
- Documenta��o (Swagger): `http://localhost:8000/docs`
- Endpoint de sa�de: `http://localhost:8000/health`

5. Caso seja necess�rio aplicar migra��es manualmente (o servi�o `migrate` tenta aplicar automaticamente no startup):

```powershell
docker compose run --rm migrate
```

6. Parar os servi�os (mantendo os dados do banco):

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

2. Instale as depend�ncias:

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
1. Instale as depend�ncias (se n�o estiver usando Docker):

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

Migra��es (Alembic)
O projeto j� possui `alembic` configurado. Para criar e aplicar migra��es:

- Criar uma revis�o autom�tica a partir dos modelos:

```powershell
alembic revision --autogenerate -m "descri��o"
```

- Aplicar migra��es localmente:

```powershell
alembic upgrade head
```

- Aplicar migra��es no Docker:

```powershell
docker compose run --rm migrate
```

Observa��o: o servi�o `migrate` utiliza o script `scripts/wait_for_db.py` para aguardar o banco antes de executar as migrations.

----

Verifica��o de sa�de (healthcheck)
- A aplica��o exp�e `GET /health` retornando `{ "status": "ok" }`. Esse endpoint � utilizado pelo `docker-compose` para verificar a sa�de do servi�o.

----

Seguran�a e boas pr�ticas
- N�o comite arquivos com credenciais (o `.env` est� listado em `.gitignore`). Para produ��o, use secrets (Docker secrets, Vault, etc.).
- Em produ��o, restrinja CORS (atualmente est� `allow_origins=["*"]` para desenvolvimento).
- Use logging estruturado em vez de `print()` para mensagens de runtime (substitui��es j� aplicadas em alguns scripts).

----

Resolu��o de problemas (r�pido)
- Se o `docker compose up` falhar no build por depend�ncias nativas (por exemplo `asyncpg`), tente rebuild sem cache:

```powershell
docker compose build --no-cache web
```

- Se as migrations falharem por timeout de conex�o, aumente `WAIT_TIMEOUT` ou execute:

```powershell
docker compose run --rm migrate
```

----
