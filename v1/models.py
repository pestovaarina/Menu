from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from .database import Base


class Menu(Base):
    __tablename__ = "menu"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    submenu = relationship("Submenu", cascade="all, delete",
                           back_populates="menu")


class Submenu(Base):
    __tablename__ = "submenu"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(String, ForeignKey("menu.id"))
    menu = relationship("Menu", back_populates="submenu")
    dishes = relationship("Dish", cascade="all, delete",
                          back_populates="submenu")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(String, ForeignKey("submenu.id"))
    submenu = relationship("Submenu", back_populates="dishes")
