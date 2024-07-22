from tests.helper.data_constants import *
from qpystructs import get_value, set_value, differ, load_from_file


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
