from sqlalchemy import create_engine, String, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.ext.indexable import index_property

from utils import EncodeLatLonSize

RESOURCE_LIST = ['Nails', 'Boards', 'Logs', 'Wire']

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
    lat: Mapped[str] = mapped_column(String(20))
    lon: Mapped[str] = mapped_column(String(20))

pc_8_index = Index('pc8_idx', ResourcePin.pc_8)
pc_10_index = Index('pc10_idx', ResourcePin.pc_10)
pc_12_index = Index('pc12_idx', ResourcePin.pc_12)

Base.metadata.create_all(engine)

def get_resource_name(resource):
    hash_int = hash(str(resource))
    mod_range = len(RESOURCE_LIST) - 1
    chosen_index = hash_int % mod_range
    return RESOURCE_LIST[chosen_index]

def add_resource_group(resource_group):
    with Session(engine) as session:
        print('add resources: ', str(resource_group))
        for resource in resource_group:
            resource_name = get_resource_name(resource)
            lat = resource.get('lat')
            lon = resource.get('lon')
            full_pluscode = EncodeLatLonSize(lat, lon)
            pc_8 = full_pluscode[0:9]
            pc_10 = full_pluscode[9:11]
            if len(full_pluscode) >= 12:
                pc_12 = full_pluscode[11:13]
            else:
                pc_12 = '22'
            resource_to_add = ResourcePin(resource_name=resource_name, pc_8=pc_8, pc_10=pc_10, pc_12=pc_12, lat=str(lat), lon=str(lon)  )
            session.add(resource_to_add)
        session.commit()