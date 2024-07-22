# README

Two ways to create a new python project:

- create project by copier:

```sh
copier copy --trust https://github.com/fluent-qa/fluentqa-pytpl.git my-project
```

- create project by pdm

```sh
mkdir my-project && cd my-project
pdm init https://github.com/fluent-qa/fluentqa-pytpl.git
```


## How to Use 

data and format:

```json
{
  "key": "v1",
  "kList": [
    "test",
    "t2"
  ],
  "kObj": {
    "k1": "v1",
    "k2": "v2"
  },
  "kBool": true,
  "kNum": 4.3
}

```

```python

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
```


```
def test_modelize_camel_naming():
    result = DemoModel.parse_file("./structured-data/camel.json")
    print(result)


def test_modelize_alias_naming():
    result = DemoModelAlias.parse_file("./structured-data/camel-alias.json")
    print(result.k_index)
    print(result.model_dump_json(by_alias=True))
    print(result.to_json())


def test_parse_as():
    result = DemoModelAlias.parse_file("./structured-data/camel-alias.json")
    json_str = result.model_dump_json(by_alias=True)
    obj_model = sr.parse_as(json_str, DemoModelAlias)
    dict_obj = result.to_dict(by_alias=True)
    print(obj_model)
    dict_model = sr.parse_as(dict_obj, DemoModelAlias)
    assert dict_model.key == "v1"


def test_parse_file_as():
    result = operations.parse_file_as("./structured-data/camel-alias.json", DemoModelAlias)
    assert result.k_index == 4.3


def test_load_csv_files():
    result = operations.parse_file_as("./structured-data/unit.csv", DemoUnit, data_format=DataFormatType.CSV)
    print(result)


def test_load_excel_file():
    result = operations.parse_file_as("./structured-data/unit_demo.xlsx", UnitInfo, data_format=DataFormatType.EXCEL)
    print(result)


def test_load_excel_file_raw():
    result = operations.parse_file_as("./structured-data/unit_demo.xlsx", UnitInfoRawModel,
                                      data_format=DataFormatType.EXCEL)
    print(result)
```