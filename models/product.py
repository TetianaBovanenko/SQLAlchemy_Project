from sqlalchemy import Column, Integer, String, Float
from models.base import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price})>"
