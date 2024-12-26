from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from app.config.database.database import Base


class Access(Base):
    __tablename__ = "access"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    refresh_token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
