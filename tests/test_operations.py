import pandas as pd

from qpystructs.operations import *
from tests.helper.data_constants import *


def test_get_value_by_expression():
    result = get_value(more_dict, "characters.Lonestar")
    assert result == {
        "id": 55923,
        "role": "renegade",
        "items": ["space winnebago", "leather jacket"],
    }


def test_set_value_by_express():
    new_dict = set_value(more_dict, "characters.Lonestar", {})
    result = get_value(new_dict, "characters.Lonestar")
    assert result == {}


def test_set_value_by_express_json():
    result = set_value(more_json_dict, "characters.Lonestar", {})
    result = get_value(result, "characters.Lonestar")
    assert result == {}


def test_differ():
    result = differ(more_dict, more_json_dict)
    print(result)
    assert len(result) > 1


def test_query_expression():
    query = "locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}"
    result = load_from_file("./structured-data/query-data.json")
    query_result = get_value(result, query)
    assert query_result == {
        "WashingtonCities": "Bellevue, Olympia, Seattle"
    }


def test_flat_json():
    data = [
        {
            "state": "Florida",
            "shortname": "FL",
            "info": {"governor": "Rick Scott"},
            "counties": [
                {"name": "Dade", "population": 12345},
                {"name": "Broward", "population": 40000},
                {"name": "Palm Beach", "population": 60000},
            ],
        },
        {
            "state": "Ohio",
            "shortname": "OH",
            "info": {"governor": "John Kasich"},
            "counties": [
                {"name": "Summit", "population": 1234},
                {"name": "Cuyahoga", "population": 1337},
            ],
        }]
    result = pd.json_normalize(
        data, "counties", ["state", "shortname", ["info", "governor"]]
    )
    print(result)
    result.to_excel("json-flat.xlsx")
    json_data = load_from_file("tmp.json")
    print(json_data)


def test_merged_cell():
    json_file_to_excel("tmp.json", 'tmp-json.xlsx')
    result = read_merged_excel("merged_cell.xlsx")
    print(result)
