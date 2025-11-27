from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, DateTime, func, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone

db = SQLAlchemy()

# Modelo principal: User

class User(db.Model):
    __tablename__="user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    name: Mapped[str | None] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default= True, nullable=False)

    # Relaciones
    posts: Mapped[list["Post"]] = relationship(back_populates="user", lazy=True)
    favorites: Mapped[list["Favorites"]] = relationship(back_populates="user", lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "favorites_count": len(self.favorites)
        }

# Modelo de asociación: Favorites (Muchos a muchos)

class Favorites(db.Model):
    __tablename__="favorites"
    # Clave Foreign a user
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    
    # Identificación del ítem favorito 
    item_type: Mapped[str] = mapped_column(String(50), primary_key=True) # 'character' o 'planet'
    item_id: Mapped[int] = mapped_column(Integer, primary_key=True) # ID del item

    # Relación de navegación
    user: Mapped["User"] = relationship(back_populates="favorites")
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "item_type": self.item_type,
            "item_id": self.item_id,
        }


# Modelo de contenido: Personajes

class Character(db.Model):
    __tablename__="character"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=False)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=False)
    height: Mapped[str] = mapped_column(String(20), nullable=False)
    mass: Mapped[str] = mapped_column(String(40), nullable=False)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=False)
    homeworld_url: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "homeworld_url": self.homeworld_url,
            "created_at": self.created_at.isoformat(),
            "edited_at": self.edited_at.isoformat() if self.edited_at else None
        }


# Modelo de contenido: Planetas

class Planet(db.Model):
    __tablename__="planet"
    id: Mapped[int] = mapped_column(primary_key=True)
    diameter: Mapped[str] = mapped_column(String(100), nullable=False)
    gravity: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False)
    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "created_at": self.created_at.isoformat(),
            "edited_at": self.edited_at.isoformat() if self.edited_at else None
        }

# Modelo de contenido: Vehicle

class Vehicle(db.Model):
    __tablename__ = "vehicle"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    crew: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "crew": self.crew,
        }


# Modelo de contenido: Post (Artículos del blog)

class Post(db.Model):
    __tablename__="post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String(5000), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Foreign a User
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    # Relación de navegación
    user: Mapped["User"] = relationship(back_populates="posts")

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user_id
        }