from sqlalchemy import (Boolean, Column, Date, Float, ForeignKey, Integer,
                        Numeric, String, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from fast_api.v1.models import BaseRow


class CancellationPolicy(BaseRow):
    __tablename__ = 'tbl_pl_cancellation_policy'

    cancellation_policy_id = Column(Integer, primary_key=True)
    cancellation_policy_name = Column(String(100))

class RoomType(BaseRow):
    __tablename__ = 'tbl_pl_room_type'

    room_type_id = Column(Integer, primary_key=True)
    room_type_name = Column(String(100))

class Host(BaseRow):
    __tablename__ = 'tbl_host'

    host_id = Column(Integer, primary_key=True)
    host_identity_verified = Column(Boolean)
    host_name = Column(String(100))

class Listing(BaseRow):
    __tablename__ = 'tbl_listings'

    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    host_id = Column(Integer, ForeignKey('tbl_host.host_id'))
    neighbourhood_group = Column(String(100))
    neighbourhood = Column(String(150))
    lat = Column(Numeric)
    long = Column(Numeric)
    instant_bookable = Column(Boolean)
    cancellation_policy_id = Column(Integer, ForeignKey('tbl_pl_cancellation_policy.cancellation_policy_id'))
    room_type_id = Column(Integer, ForeignKey('tbl_pl_room_type.room_type_id'))
    construction_year = Column(Integer)
    price = Column(Integer)
    service_fee = Column(Integer)
    minimum_nights = Column(Integer)
    number_of_reviews = Column(Integer)
    last_review = Column(Date)
    reviews_per_month = Column(Float(2))
    review_rate_number = Column(Integer)
    calculated_host_listings_count = Column(Integer)
    availability_365 = Column(Integer)
    house_rules = Column(Text)

    host = relationship("Host")
    cancellation_policy = relationship("CancellationPolicy")
    room_type = relationship("RoomType")