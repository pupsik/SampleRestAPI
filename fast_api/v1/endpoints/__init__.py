from sqlalchemy.orm import Session

from fast_api.v1.settings import SESSION


def get_db_session() -> Session:
    with SESSION() as session:
        yield session
