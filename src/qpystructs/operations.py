from __future__ import annotations

import copy
import csv
import enum
import json
from pathlib import Path
from typing import TypeVar, Union, Any, List, Dict

import yaml
import jmespath

from qpystructs import GenericDataModel
from pydantic import BaseModel
import pandas as pd
from deepdiff import DeepDiff

from .dotty import dotty


class DataFormatType(enum.Enum):
    JSON = 1
    DICT = 2
    YAML = 3
    XML = 4
    CSV = 5
    TSV = 6
    SQL = 7
    TOML = 8
    EXCEL = 9


T = TypeVar("T", bound=Union[GenericDataModel, BaseModel])  # Declare type variable


def parse_as(
        json_or_dict: str | dict, to_type: T
) -> Union[GenericDataModel, BaseModel, Any]:
    """
    parse_as: takes a string or a dict and turns it into a GenericDataModel
    @param json_or_dict: either a string or a dict
    @param to_type: the type of generic data
    """
    if isinstance(json_or_dict, str):
        return to_type.parse_raw(json_or_dict)
    else:
        return to_type.parse_obj(json_or_dict)


def to_json(obj: Union[GenericDataModel, BaseModel]) -> str:
    """
    to_json: model to json
    """
    if isinstance(obj, GenericDataModel):
        return obj.to_json()
    else:
        return obj.model_dump_json(by_alias=True, exclude_none=True)


def load_from_file(file_path: Path | str, data_format=DataFormatType.JSON) -> Any:
    match data_format:
        case DataFormatType.JSON:
            with open(file_path, "r") as f:
                return json.load(f)
        case DataFormatType.YAML:
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        case DataFormatType.CSV:
            with open(file_path, "r") as f:
                return csv.DictReader(f)
        case DataFormatType.EXCEL:
            return pd.read_excel(file_path)
        case _:
            raise ValueError(f" data format: {data_format} is not supported")


def dataframe_to_model(df: pd.DataFrame, to_type: T | Dict | dict = Dict) -> list[dict] | list[Any]:
    if to_type is Dict or to_type is dict:
        return df.to_dict()
    t_list = []
    for index, row in df.iterrows():
        t_list.append(to_type(**row.to_dict()))
    return t_list


# 1. string/file=>convert to model
# 2. get value from structured data
def parse_file_as(file_path: Path | str, to_type: T, data_format=DataFormatType.JSON,
                  sheet_name=None) -> T | List[T]:
    match data_format:
        case DataFormatType.JSON:
            with open(file_path, "r") as f:
                content = f.read()
                return to_type.model_validate_json(content)
        case DataFormatType.YAML:
            with open(file_path, "r") as f:
                content = yaml.safe_load(f)
                return to_type.model_validate(content)
        case DataFormatType.CSV:
            result = pd.read_csv(file_path, na_filter=False, na_values=['NaN'])
            return dataframe_to_model(result, to_type)

        case DataFormatType.EXCEL:
            if sheet_name is None:
                result = pd.read_excel(file_path, na_filter=False, na_values=['NaN'])
            else:
                result = pd.read_excel(file_path, sheet_name=sheet_name, na_filter=False, na_values=['NaN'])
            return dataframe_to_model(result, to_type)

        case _:
            raise ValueError(f" data format: {data_format} is not supported")


def get_value(target_object: str | dict | BaseModel | GenericDataModel, path_exp: str,
              **kwargs) -> Any:
    if isinstance(target_object, Dict):
        return jmespath.search(expression=path_exp, data=target_object)
    if isinstance(target_object, str):
        return jmespath.search(data=json.loads(target_object), expression=path_exp)
    if isinstance(target_object, BaseModel):
        return jmespath.search(data=target_object.dict(), expression=path_exp)

    raise NotImplementedError("not support type " + type(target_object))


def set_value(json_dict: Union[str, Dict], path_exp: str, to_value: Any) -> Dict:
    """
    set new value in a dict, return a new dict with new value
    """
    dict_value = copy.deepcopy(json_dict)
    if isinstance(json_dict, str):
        dict_value = json.loads(dict_value)
    dot = dotty(dict_value)
    dot[path_exp] = to_value
    return dot.to_dict()


class DifferModel(GenericDataModel):
    category: str
    difference: dict | Any


def extract_obj_diff(difference: DeepDiff) -> List[DifferModel]:
    result = []
    for key, value in difference.items():
        result.append(DifferModel(category=key, difference=value))
    return result


def differ(expected_data: Union[str, dict], actual_data: Union[str, dict]):
    if isinstance(expected_data, str):
        v1 = json.loads(expected_data)
    else:
        v1 = expected_data
    if isinstance(actual_data, str):
        v2 = json.loads(actual_data)
    else:
        v2 = actual_data
    return extract_obj_diff(DeepDiff(v1, v2, verbose_level=2))


def json_file_to_excel(json_file, excel_file):
    """
    json file to excel
    """
    json_data = load_from_file(json_file)
    json_data_df = pd.json_normalize(json_data)
    json_data_df.to_excel(excel_file)


def read_merged_excel(excel_path):
    """
    read merged cell excel file
    """
    raw_df = pd.read_excel(excel_path)
    raw_df.fillna("fillna", inplace=True)
    return raw_df
