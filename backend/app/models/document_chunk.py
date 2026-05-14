from sqlalchemy import (
    Column,
    Integer,
    Text
)

from sqlalchemy.dialects.postgresql import (
    JSONB
)

from app.models.base import (
    Base
)


class DocumentChunk(Base):

    __tablename__ = (
        "document_chunks"
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    content = Column(
        Text,
        nullable=False
    )

    document_metadata = Column(
        JSONB,
        nullable=True
    )