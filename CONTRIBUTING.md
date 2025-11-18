# Contribuindo

Obrigado por contribuir com o projeto! Este documento descreve o fluxo mínimo recomendado para alterações, especialmente para mudanças no schema do banco.

## Fluxo mínimo para mudanças no schema (muito importante)
1. Crie uma branch a partir de `main` com nome descritivo: `feature/xxx` ou `bugfix/xxx`.
2. Atualize/adicione os models em `app/models/`.
3. Gere uma migration autogerada:

```powershell
docker compose run --rm web alembic revision --autogenerate -m "Descrição curta da mudança"
```

4. Revise o arquivo gerado em `alembic/versions/` — corrija nomes de FK, índices e constraints manualmente quando necessário.
5. Rode os testes localmente (ou via container) e verifique o banco em ambiente de dev:

```powershell
docker compose run --rm web sh -c "pip install pytest && pytest -q"
```

6. Commit suas mudanças (models + migration) e abra o Pull Request.

## Template mínimo de Pull Request
- Título: curto e descritivo, ex.: `feat(model): adicionar tabela usuarios`
- Descrição:
  - O que foi alterado
  - Por que a mudança é necessária
  - Passos para testar (comandos rápidos)
  - Links para issues relacionadas (se houver)

Exemplo:

```
Título: feat(model): adicionar tabela usuarios

Descrição:
- Adiciona model `Usuario` com campos: id, nome, email
- Gera migration `0002_add_usuario` (revisada)

Como testar:
1. docker compose run --rm web alembic upgrade head
2. docker compose run --rm web sh -c "pip install pytest && pytest -q"

Issue: #12
```

## Boas práticas
- Sempre rode os testes antes de abrir o PR.
- Revise migrations geradas automaticamente.
- Não aplique migrations sem revisão.

