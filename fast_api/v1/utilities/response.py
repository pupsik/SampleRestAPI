import json
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class CustomJSONResponse(JSONResponse):
    def __init__(self, *args, encoder=None, **kwargs):
        self.encoder = encoder
        super().__init__(*args, **kwargs)

    def render(self, content: Any) -> bytes:
        return json.dumps(
            obj=content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            cls=self.encoder,
            separators=(",", ":"),
        ).encode("utf-8")
