from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class CapturaFrame(Base):
    """Modelo para tabela `captura_frame`.

    Repare que `id_frame` é a primary key (Integer autoincrement).
    Campos numéricos como `frame_index` e `faces_count` são `Integer`.
    Use `Float` para valores contínuos (ex.: métricas de confiança).
    """

    __tablename__ = "captura_frame"

    id_frame: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    documento_id: Mapped[int] = mapped_column(Integer, nullable=True)  # possível FK para documentos.id
    frame_index: Mapped[int] = mapped_column(Integer, nullable=False)
    timestamp_ms: Mapped[int] = mapped_column(Integer, nullable=True)  # milissegundos do vídeo
    path: Mapped[str] = mapped_column(String(512), nullable=True)
    faces_count: Mapped[int] = mapped_column(Integer, nullable=True)
    mean_confidence: Mapped[float] = mapped_column(Float, nullable=True)
    id_engajamento: Mapped[int] = mapped_column(Integer, ForeignKey("engajamento_documento.id_engajamento"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("now()"), nullable=False)

    def __repr__(self) -> str:
        return f"<CapturaFrame(id={self.id_frame}, frame_index={self.frame_index}, id_engajamento={self.id_engajamento})>"
