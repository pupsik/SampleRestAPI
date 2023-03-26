from dataclasses import dataclass, field

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, func, select, update

from fast_api.v1.models.db import Listing, RoomType
from fast_api.v1.models.request import UpdateListing
from fast_api.v1.models.response import HelloWorldResponse
from fast_api.v1.settings import SESSION
from fast_api.v1.utilities.encoders import CustomJSONEncoder
from fast_api.v1.utilities.response import CustomJSONResponse


@dataclass
class Endpoint:
    prefix: str
    router: APIRouter = field(default_factory=APIRouter)


endpoint = Endpoint(prefix="/api")


@endpoint.router.get("/", include_in_schema=False)
async def read_home() -> HelloWorldResponse:
    return {"hello": "world"}


@endpoint.router.get("/property/summary")
async def get_property_summary():
    stmt = select(
        Listing.neighbourhood,
        func.count(Listing.id),
        func.avg(Listing.price),
    ).group_by(Listing.neighbourhood)
    with SESSION() as session:
        result = session.execute(stmt).all()
        data = [
            {"id": id, "avg_price": price, "neighbourhood": neighbourhood}
            for id, price, neighbourhood in result
        ]
    return CustomJSONResponse(
        status_code=status.HTTP_200_OK,
        content=data,
        encoder=CustomJSONEncoder,
    )


@endpoint.router.get("/property/list")
async def get_properties(
    name: str = None,
    neighbourhood: str = None,
    room_type_name: str = None,
):
    qmap = {
        "name": Listing.name.ilike(f"%{name}%") if name is not None else None,
        "neighbourhood": Listing.neighbourhood.ilike(f"%{neighbourhood}%")
        if neighbourhood is not None
        else None,
        "room_type_name": RoomType.room_type_name.ilike(f"%{room_type_name}%")
        if room_type_name is not None
        else None,
    }
    conditions = [condition for condition in qmap.values() if condition is not None]

    stmt = select(
        Listing.id, Listing.name, Listing.neighbourhood, RoomType.room_type_name
    ).join(RoomType)

    if conditions:
        stmt = stmt.where(and_(*conditions))

    with SESSION() as session:
        result = session.execute(stmt).all()
        data = [
            {
                "id": id,
                "name": name,
                "neighbourhood": neighbourhood,
                "room_type_name": room_type_name,
            }
            for id, name, neighbourhood, room_type_name in result
        ]
    return CustomJSONResponse(
        status_code=status.HTTP_200_OK,
        content=data,
        encoder=CustomJSONEncoder,
    )


@endpoint.router.get("/property/{id}")
async def get_property_by_id(id: int):
    stmt = select(Listing).where(Listing.id.in_([id]))

    with SESSION() as session:
        listing = session.execute(stmt).first()

    if not listing:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=f"Property with {id} does not exist",
        )

    return CustomJSONResponse(
        status_code=status.HTTP_200_OK,
        content=listing[0].to_dict(),
        encoder=CustomJSONEncoder,
    )


@endpoint.router.put("/property/{id}")
async def update_property_by_id(id: int, property: UpdateListing):
    stmt = (
        update(Listing)
        .where(Listing.id == id)
        .values({k: v for k, v in property.dict(exclude_unset=True).items()})
    )
    with SESSION() as session:
        with session.begin():
            session.execute(stmt)

        with session.begin():
            stmt = select(Listing).where(Listing.id.in_([id]))
            listing = session.execute(stmt).first()[0].to_dict()

    return CustomJSONResponse(
        status_code=status.HTTP_200_OK,
        content=listing,
        encoder=CustomJSONEncoder,
    )
