from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class ExpressoesCorporal(Base):
    """Modelo para tabela `expressoes_corporal`.

    Observação: adicione os campos exatos que deseja abaixo. O campo
    `id_expressao_c` é a chave primária e já está definido.
    """

    id_expressao_c: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Exemplo de campos: ajuste conforme o schema que você enviar
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    intensidade: Mapped[float] = mapped_column(Float, nullable=True)
    frequencia: Mapped[int] = mapped_column(Integer, nullable=True)
    id_engajamento: Mapped[int] = mapped_column(Integer, ForeignKey("engajamento_documento.id_engajamento"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False)

    def __repr__(self) -> str:  # ajuda no debug
        return f"<ExpressoesCorporal(id={self.id_expressao_c}, nome={self.nome}, id_engajamento={self.id_engajamento})>"
