 # confereAi API

 Este repositório contém uma API em FastAPI e suporte para banco PostgreSQL (asyncpg + SQLAlchemy). Abaixo estão instruções completas para rodar localmente, com Docker, executar/migrar o banco e como alterar o schema.

 **Resumo rápido (recomendado)**
 - Recomendado: usar Docker Compose para desenvolvimento (levanta Postgres, aplica migrações e roda a aplicação).
 - Alternativa local: venv + instalar dependências (pode exigir ferramentas de compilação no Windows para `asyncpg`).

 **Requisitos**
 - Docker e Docker Compose (recomendado)
 - Python 3.11 (recomendado para ambiente local)

 **1) Preparar variáveis de ambiente**
 - Copie o `.env.example` para `.env` e ajuste conforme necessário:
 ```powershell
 cp .env.example .env
 ```
 - A variável mais importante é `DATABASE_URL`. Exemplo para Docker Compose (já definido no `docker-compose.yml`):
 ```text
 postgresql+asyncpg://confere:confere@db:5432/confere
 ```

 **2) Rodar com Docker Compose (recomendado)**
 - Build e start (vai criar rede, volume, container do Postgres, da app e um container `migrate` para as migrações):
 ```powershell
 docker compose up --build
 # ou em background
 docker compose up -d --build
 ```
 - Logs (verificar status e migrações):
 ```powershell
 docker compose logs --tail 200
 docker compose ps
 ```
 - A aplicação ficará disponível em `http://localhost:8000` (o `web` expõe `8000:80` no `docker-compose.yml`).

 **3) Run migrations (Alembic)**
 - O `docker-compose.yml` já inclui o serviço `migrate` que roda `alembic upgrade head`.
 - Para rodar manualmente dentro do container (útil após alterar migrations):
 ```powershell
 docker compose run --rm migrate
 # ou executar a partir da imagem web
 docker compose run --rm web alembic upgrade head
 ```
 - Para criar uma nova migration a partir de mudanças nos models:
 ```powershell
 # abra um shell no container web (ou usar localmente com venv)
 docker compose run --rm web alembic revision --autogenerate -m "descrição"
 # revise o arquivo gerado em alembic/versions, depois aplique
 docker compose run --rm migrate
 ```

 **4) Acessar o banco para inspeção/edição (psql)**
 - Conectar ao Postgres do container:
 ```powershell
 docker compose exec db psql -U confere -d confere
 ```
 - Criar/alterar dados manualmente via `psql` ou rodar scripts SQL em `/docker-entrypoint-initdb.d` (apenas na primeira inicialização do volume).

 **5) Rodar localmente sem Docker (desenvolvimento)**
 - Recomendado somente para desenvolvimento rápido; Docker evita problemas de compilação de dependências nativas no Windows.
 ```powershell
 python -m venv .venv
 .\.venv\Scripts\Activate.ps1
 python -m pip install --upgrade pip
 pip install -r requirements.txt
 # Se a instalação de asyncpg falhar no Windows, veja seção Troubleshooting
 ```
 - Rodar testes:
 ```powershell
 .\.venv\Scripts\Activate.ps1
 pip install pytest
 python -m pytest app/tests -q
 ```
 - Rodar servidor local (uvicorn):
 ```powershell
 .\.venv\Scripts\Activate.ps1
 uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
 ```

 **6) Criar tabelas sem Alembic (dev)**
 - Há um helper assíncrono que executa `Base.metadata.create_all()`:
 ```powershell
 # via Docker (recomendado)
 docker compose exec web python -c "import asyncio; from app.db.init_db import init_db; asyncio.run(init_db())"

 # ou local (venv)
 .\.venv\Scripts\Activate.ps1
 python -c "import asyncio; from app.db.init_db import init_db; asyncio.run(init_db())"
 ```

 **7) Fluxo recomendado para alterar o schema (melhor prática)**
 1. Atualize/adicione seus models em `app/models/*.py`.
 2. Gere uma migration autogerada:
	```powershell
	docker compose run --rm web alembic revision --autogenerate -m "Minha mudança"
	```
 3. Revise o arquivo em `alembic/versions/` (corrija se necessário).
 4. Aplique a migration:
	```powershell
	docker compose run --rm migrate
	```
 5. Verifique logs e integridade do banco (`psql` ou ferramentas de DB GUI).

 **8) Comandos úteis de manutenção**
 - Parar e remover containers (mantendo dados):
 ```powershell
 docker compose down
 ```
 - Parar e remover containers + volumes (limpa dados):
 ```powershell
 docker compose down -v
 ```
 - Rebuild quando alterar `requirements.txt` ou Dockerfile:
 ```powershell
 docker compose build --no-cache
 docker compose up -d --build
 ```

 **9) Troubleshooting comum**
 - Erro ao instalar `asyncpg` no Windows (compilação falha):
   - Causa: `asyncpg` pode precisar das Microsoft C++ Build Tools para compilar extensões C/Cython.
   - Soluções:
	 - Use Docker (imagem Linux) — a maioria dos pacotes instala wheels prontos.
	 - Instale o Visual C++ Build Tools (link no erro do pip) e reexecute `pip install -r requirements.txt`.
	 - Use Python 3.11 ou 3.12 (versões com wheels disponíveis para `asyncpg`) — o projeto recomenda Python 3.11.
	 - Alternativa temporária: remover `asyncpg` de `requirements.txt` e instalar apenas no ambiente de produção.

 - `alembic` não encontra o pacote `app` dentro do container migrate:
   - Solução aplicada neste repositório: `Dockerfile` define `ENV PYTHONPATH=/app` para garantir que `import app` funcione nos containers.

 **10) Notas finais e dicas**
 - O `docker-compose.yml` já inclui `db`, `web` e `migrate` (migrate roda `alembic upgrade head`).
 - Prefira usar Docker Compose para evitar problemas de dependências nativas em diferentes OS.
 - Sempre revise as migrations geradas automaticamente antes de aplicá-las.

 Se quiser, eu posso:
 - Gerar um `.env.example` com valores seguros de exemplo (se ainda não existir).
 - Remover o arquivo temporário `debug_migrate.py` criado para debug.
 - Abrir um PR com as mudanças (incluindo este README e `Dockerfile` ajustado).

