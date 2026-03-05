from sqlalchemy import Column, Integer, String, Text, Enum
from .database import Base
import enum

class SafetyRating(enum.Enum):
    SAFE = "Safe"
    MODERATE = "Moderate"
    IRRITANT = "Irritant"
    AVOID = "Avoid"

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    safety_rating = Column(Enum(SafetyRating), nullable=False)
    # The skin types it might be good or bad for, stored as a simple string or JSON string.
    compatible_skin_types = Column(String(500), nullable=True)
    
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    brand = Column(String(255), nullable=True)
    ingredients_list = Column(Text, nullable=False)
