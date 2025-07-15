from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal


# Persistent models (stored in database)
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    food_entries: List["FoodEntry"] = Relationship(back_populates="user")


class FoodItem(SQLModel, table=True):
    __tablename__ = "food_items"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200, index=True)
    calories_per_100g: Decimal = Field(decimal_places=2, max_digits=8)
    brand: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    food_entries: List["FoodEntry"] = Relationship(back_populates="food_item")


class FoodEntry(SQLModel, table=True):
    __tablename__ = "food_entries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    food_item_id: int = Field(foreign_key="food_items.id")
    quantity_grams: Decimal = Field(decimal_places=2, max_digits=8)
    total_calories: Decimal = Field(decimal_places=2, max_digits=8)
    consumed_at: datetime = Field(default_factory=datetime.utcnow)
    entry_date: date = Field(default_factory=date.today, index=True)

    user: User = Relationship(back_populates="food_entries")
    food_item: FoodItem = Relationship(back_populates="food_entries")


class DailySummary(SQLModel, table=True):
    __tablename__ = "daily_summaries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    summary_date: date = Field(index=True)
    total_calories: Decimal = Field(decimal_places=2, max_digits=10, default=Decimal("0"))
    total_entries: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Unique constraint for user and date combination
    __table_args__ = ({"schema": None},)


# Non-persistent schemas (for validation, forms, API requests/responses)
class UserCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)


class FoodItemCreate(SQLModel, table=False):
    name: str = Field(max_length=200)
    calories_per_100g: Decimal = Field(decimal_places=2, max_digits=8)
    brand: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)


class FoodItemUpdate(SQLModel, table=False):
    name: Optional[str] = Field(default=None, max_length=200)
    calories_per_100g: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    brand: Optional[str] = Field(default=None, max_length=100)
    category: Optional[str] = Field(default=None, max_length=50)


class FoodEntryCreate(SQLModel, table=False):
    user_id: int
    food_item_id: int
    quantity_grams: Decimal = Field(decimal_places=2, max_digits=8)


class FoodEntryUpdate(SQLModel, table=False):
    quantity_grams: Optional[Decimal] = Field(default=None, decimal_places=2, max_digits=8)
    consumed_at: Optional[datetime] = Field(default=None)


class DailyCaloriesSummary(SQLModel, table=False):
    date: date
    total_calories: Decimal
    total_entries: int
    entries: List["FoodEntryWithDetails"]


class FoodEntryWithDetails(SQLModel, table=False):
    id: int
    food_name: str
    brand: Optional[str]
    quantity_grams: Decimal
    total_calories: Decimal
    consumed_at: datetime
    calories_per_100g: Decimal
