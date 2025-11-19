from datetime import datetime
from sqlalchemy import Integer, String, DateTime, text
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class Teste(Base):
    """Modelo mínimo para tabela `relatorio` referenciada por FKs."""

    __tablename__ = "teste"

    id_relatorio: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False)

    def __repr__(self) -> str:
        return f"<Relatorio(id={self.id_relatorio}, titulo={self.titulo})>"
