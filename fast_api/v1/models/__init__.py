from sqlalchemy.orm import DeclarativeBase


class BaseRow(DeclarativeBase):
    __abstract__ = True

    def __repr__(self):

        values = str(
            ",".join(
                [
                    (
                        f"{r.__str__().split('.')[1]}={getattr(self, r.__str__().split('.')[1])}"
                    )
                    for r in self.__table__.columns
                ]
            )
        )
        return f"{self.__class__.__name__}({values})"

    def to_dict(self):
        dict_ = {}
        for r in self.__table__.columns:
            dict_[r.__str__().split(".")[1]] = getattr(self, r.__str__().split(".")[1])
        return dict_