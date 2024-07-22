from __future__ import annotations

from typing import Any, Annotated

from qpystructs.models import GenericDataModel
from pydantic import BaseModel, Field,ConfigDict


#
# {
#   "key": "v1",
#   "kList": [
#     "test",
#     "t2"
#   ],
#   "kObj": {
#     "k1": "v1",
#     "k2": "v2"
#   },
#   "kBool": true,
#   "kNum": 4.3
# }

class DemoModel(GenericDataModel):
    key: str
    k_list: []
    k_obj: Any
    k_bool: bool
    k_num: float


class DemoModelAlias(GenericDataModel):
    key: str
    k_list: []
    k_obj: Any
    k_bool: bool
    # k_index: float = Field(alias='k_num')
    k_index: Annotated[float, Field(alias='kNum')]


class DemoUnit(GenericDataModel):
    unit_group_name: str | None = ""
    unit_name: str | None = ""
    unit_symbol: str | None = ""
    unit_latex: str | None = ""
    base_unit: str | None = ""
    factor: str | None = ""


class UnitInfoRawModel(BaseModel):
    unit_name: str = Field("", alias='单位名')
    unit_symbol: str = Field("", alias='单位符号')
    unit_symbol_latex: str = Field("", alias='单位符号LaTex')
    unit_group_name: str = Field("", alias='单位组名称')
    base_unit: str = Field("", alias='基准单位')
    conversion_factor: None|str |float = Field("", alias='换算系数')

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        use_enum_values=True,
    )

class UnitInfo(GenericDataModel):
    unit_name: str = Field("", alias='单位名')
    unit_symbol: str = Field("", alias='单位符号')
    unit_symbol_latex: str = Field("", alias='单位符号LaTex')
    unit_group_name: str = Field("", alias='单位组名称')
    base_unit: str = Field("", alias='基准单位')
    conversion_factor: None|str |float = Field("", alias='换算系数')