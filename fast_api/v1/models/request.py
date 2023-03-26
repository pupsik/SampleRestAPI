from typing import Optional
from pydantic import BaseModel

class UpdateListing(BaseModel):
    name: Optional[str]
    neighbourhood: Optional[str]
    instant_bookable: Optional[bool]
    cancellation_policy_id: Optional[int]
    room_type_id: Optional[int]
    construction_year: Optional[int]
    price: Optional[int]
    service_fee: Optional[int]
    minimum_nights: Optional[int]
    availability_365: Optional[int]
    house_rules: Optional[str]