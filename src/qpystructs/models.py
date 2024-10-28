from __future__ import annotations

from pathlib import Path
from typing import TypeVar, Any
from typing import Union

import re

import inflection

from pydantic import BaseModel
from pydantic import ConfigDict


def to_camel(s: str) -> str:
    s = re.sub("_(url)$", lambda m: f"_{m.group(1).upper()}", s)
    return inflection.camelize(s, uppercase_first_letter=False)


class CamelModel(BaseModel):
    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        super().__init__(**kwargs)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True,
    )

    def to_json(self, by_alias=True):
        return self.model_dump_json(by_alias=by_alias, exclude_none=True)

    def to_dict(self, by_alias=True):
        return self.model_dump(by_alias=by_alias, exclude_none=True)


class GenericDataModel(CamelModel, BaseModel):
    pass

