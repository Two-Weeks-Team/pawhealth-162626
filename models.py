import os
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Date,
    Interval,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine

# ---------------------------------------------------------------------------
# Database URL handling with auto‑fix for common DO strings
# ---------------------------------------------------------------------------
_db_url = (
    os.getenv("DATABASE_URL")
    or os.getenv("POSTGRES_URL")
    or "sqlite:///./app.db"
)
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

_connect_args = {}
if not _db_url.startswith("sqlite"):
    # Enforce SSL for remote hosts (DigitalOcean managed Postgres)
    if "localhost" not in _db_url and "127.0.0.1" not in _db_url:
        _connect_args["sslmode"] = "require"

engine = create_engine(_db_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# ---------------------------------------------------------------------------
# Table name prefix – prevents collisions in shared DBs
# ---------------------------------------------------------------------------
_TABLE_PREFIX = "pawhealth_162626_"


class User(Base):
    __tablename__ = f"{_TABLE_PREFIX}users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")


class Pet(Base):
    __tablename__ = f"{_TABLE_PREFIX}pets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}users.id"), nullable=False)
    name = Column(String(50), nullable=False)
    species = Column(String(20), nullable=False)  # e.g., dog, cat
    breed = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)  # years
    weight = Column(Float, nullable=True)  # kg
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    owner = relationship("User", back_populates="pets")
    symptoms = relationship("Symptom", back_populates="pet", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="pet", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="pet", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="pet", cascade="all, delete-orphan")
    ai_insights = relationship("AIInsight", back_populates="pet", cascade="all, delete-orphan")


class Symptom(Base):
    __tablename__ = f"{_TABLE_PREFIX}symptoms"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}pets.id"), nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Float, nullable=False)  # 0‑1 scale
    ai_analysis = Column(Boolean, default=False, nullable=False)
    ai_result = Column(Text, nullable=True)
    ai_confidence = Column(Float, nullable=True)
    ai_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pet = relationship("Pet", back_populates="symptoms")


class Meal(Base):
    __tablename__ = f"{_TABLE_PREFIX}meals"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}pets.id"), nullable=False)
    meal_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    food_type = Column(String(50), nullable=False)
    portion_size = Column(String(20), nullable=False)
    is_regular = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pet = relationship("Pet", back_populates="meals")


class Activity(Base):
    __tablename__ = f"{_TABLE_PREFIX}activities"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}pets.id"), nullable=False)
    activity_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    activity_type = Column(String(50), nullable=False)
    duration = Column(Interval, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pet = relationship("Pet", back_populates="activities")


class Medication(Base):
    __tablename__ = f"{_TABLE_PREFIX}medications"
    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}pets.id"), nullable=False)
    name = Column(String(100), nullable=False)
    dosage = Column(String(50), nullable=False)
    frequency = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pet = relationship("Pet", back_populates="medications")


class AIInsight(Base):
    __tablename__ = f"{_TABLE_PREFIX}ai_insights"
    id = Column(Integer, primary_key=True, index=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    pet_id = Column(Integer, ForeignKey(f"{_TABLE_PREFIX}pets.id"), nullable=False)
    insight_type = Column(String(50), nullable=False)
    recommendation = Column(Text, nullable=True)
    confidence = Column(Float, nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    pet = relationship("Pet", back_populates="ai_insights")

# Create all tables (useful for quick demo; in production migrations are recommended)
Base.metadata.create_all(bind=engine)
