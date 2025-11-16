from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class ExpressoesFaciais(Base):
    """Modelo para tabela `expressoes_faciais`.

    Campo `id_expressao_f` definido como PK (Integer, autoincrement).
    Ajuste/adicione os campos conforme o schema que será fornecido.
    """

    id_expressao_f: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Exemplos de campos (ajuste conforme necessário)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    intensidade: Mapped[float] = mapped_column(Float, nullable=True)
    frequencia: Mapped[int] = mapped_column(Integer, nullable=True)
    id_engajamento: Mapped[int] = mapped_column(Integer, ForeignKey("engajamento_documento.id_engajamento"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False)

    def __repr__(self) -> str:
        return f"<ExpressoesFaciais(id={self.id_expressao_f}, nome={self.nome}, id_engajamento={self.id_engajamento})>"
