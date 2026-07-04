from sqlalchemy import create_engine, String, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.indexable import index_property

engine = create_engine("sqlite:///mapgame.db")

class Base(DeclarativeBase):
    pass

class ResourcePin(Base):
    __tablename__ = "resource_pins"

    id: Mapped[int] = mapped_column(primary_key=True)
    resource_name: Mapped[str] = mapped_column(String(30))
    pc_8: Mapped[str] = mapped_column(String(8))
    pc_10: Mapped[str] = mapped_column(String(2))
    pc_12: Mapped[str] = mapped_column(String(2))
    lat: Mapped[float] = mapped_column()
    lon: Mapped[float] = mapped_column()

pc_8_index = Index('pc8_idx', ResourcePin.pc_8)
pc_10_index = Index('pc10_idx', ResourcePin.pc_10)
pc_12_index = Index('pc12_idx', ResourcePin.pc_12)

Base.metadata.create_all(engine)