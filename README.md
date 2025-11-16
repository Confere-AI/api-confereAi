# confereAi API

Este repositório contém uma API em FastAPI. Para desenvolvimento local com um banco PostgreSQL em container, usamos `docker-compose`.

## Requisitos
- Docker e Docker Compose
- Python 3.11 (para desenvolver localmente)

## Como rodar com Docker Compose
1. Copie o `.env.example` para `.env` e ajuste se necessário:
	```powershell
	cp .env.example .env
	```
2. Inicie os serviços (API + Postgres):
	```powershell
	docker compose up -d --build
	```
3. A API ficará disponível em `http://localhost:8000`.

### Variáveis de ambiente importantes
- `DATABASE_URL` — string de conexão SQLAlchemy, por exemplo: `postgresql+asyncpg://confere:confere@db:5432/confere`

## Migrações (Alembic)
As dependências incluem `alembic`. Para inicializar e executar migrações:

1. Crie a pasta de migrações (se ainda não existir):
	```powershell
	alembic init alembic
	```
2. Configure `alembic.ini` e `alembic/env.py` para usar `DATABASE_URL` e o `Base` do `app.models.base`.
	> Observação: o `alembic/env.py` já importa `app.models` para que o `metadata` dos models seja visível durante o autogerate.
3. Para criar uma migração automática a partir dos models:
	```powershell
	alembic revision --autogenerate -m "create initial tables"
	```
4. Para aplicar migrações:
	 - Local (se `DATABASE_URL` estiver configurado no host):
		 ```powershell
		 alembic upgrade head
		 ```
	 - Em Docker Compose (recomendado):
		 ```powershell
		 # Roda as migrations dentro do container `migrate` e encerra
		 docker compose run --rm migrate
		 # ou (se preferir executar a partir da imagem web):
		 docker compose run --rm web alembic upgrade head
		 ```

Se quiser, eu posso gerar os arquivos iniciais do Alembic já configurados.

## Criar tabelas sem Alembic (dev)
Se você prefere criar tabelas rapidamente sem usar Alembic, há um helper assíncrono:

```powershell
docker compose exec web python -c "import asyncio; from app.db.init_db import init_db; asyncio.run(init_db())"
```

Isso executa `Base.metadata.create_all()` usando o engine assíncrono — útil para desenvolvimento rápido.
