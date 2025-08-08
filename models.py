from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Favorite(Base):
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    toy_name = Column(String)
    toy_image = Column(String)
    toy_price = Column(String)

class User(Base):
    __tablename__ = "users"  # ОБЯЗАТЕЛЬНО два подчеркивания с каждой стороны!

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))  # Указание максимальной длины
    last_name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    favorites = relationship("Favorite", back_populates="user")