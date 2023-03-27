from typing import List

from pydantic import BaseModel


class HelloWorldResponse(BaseModel):
    hello: str


class ExceptionMessage(BaseModel):
    message: str


class PropertySummary(BaseModel):
    id: int
    avg_price: float
    neighbourhood: str


class PropertySummaryList(BaseModel):
    property_summaries: List[PropertySummary]


class Property(BaseModel):
    id: int
    name: str
    neighbourhood: str
    room_type_name: str


class PropertyList(BaseModel):
    properties: List[Property]


class PropertyRecord(BaseModel):
    id: int
    name: str
    host_id: int
    latitude: float
    longitude: float
    room_type_id: int
    price: float
    minimum_nights: int
    number_of_reviews: int
    last_review: str
    reviews_per_month: float
    calculated_host_listings_count: int
    availability_365: int
    neighbourhood: str
