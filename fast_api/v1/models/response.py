from pydantic import BaseModel


class HelloWorldResponse(BaseModel):
    hello: str


class ExceptionMessage(BaseModel):
    message: str
