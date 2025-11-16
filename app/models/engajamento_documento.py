from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class EngajamentoDocumento(Base):
    """Modelo para tabela `engajamento_documento`.

    `id_engajamento` é a chave primária (Integer, autoincrement). Ajuste os
    campos numéricos conforme seu schema (Float vs Integer vs Numeric).
    """

    id_engajamento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # Exemplo de campos: atualize conforme o schema que você enviar
    documento_id: Mapped[int] = mapped_column(Integer, nullable=True)  # FK sugerida para `documentos.id`
    id_relatorio: Mapped[int] = mapped_column(Integer, ForeignKey("relatorio.id_relatorio"), nullable=True)
    visualizacoes: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    curtidas: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    probabilidade_compartilhamento: Mapped[float] = mapped_column(Float, nullable=True)
    tempo_medio: Mapped[float] = mapped_column(Float, nullable=True)  # segundos, por exemplo
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False)

    def __repr__(self) -> str:
        return f"<EngajamentoDocumento(id={self.id_engajamento}, documento_id={self.documento_id}, relatorio_id={self.id_relatorio})>"
