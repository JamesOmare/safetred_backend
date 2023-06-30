from datetime import datetime
from pydantic import Field
from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class Timestamp:
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modified_at: datetime = Field(
        sa_column=Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.now, nullable=False)
    )