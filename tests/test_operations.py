import qpystructs
from data_constants import more_dict, more_json_dict


def test_get_value_by_expression():
    result = qpystructs.get_value(more_dict, "characters.Lonestar")
    assert result == {
        "id": 55923,
        "role": "renegade",
        "items": ["space winnebago", "leather jacket"],
    }


def test_set_value_by_express():
    new_dict = qpystructs.set_value(more_dict, "characters.Lonestar", {})
    result = qpystructs.get_value(new_dict, "characters.Lonestar")
    assert result == {}


def test_set_value_by_express_json():
    result = qpystructs.set_value(more_json_dict, "characters.Lonestar", {})
    result = qpystructs.get_value(result, "characters.Lonestar")
    assert result == {}


def test_differ():
    result = qpystructs.differ(more_dict, more_json_dict)
    print(result)
    assert len(result) > 1


def test_query_expression():
    query = "locations[?state == 'WA'].name | sort(@) | {WashingtonCities: join(', ', @)}"
    result = qpystructs.load_from_file("./structured-data/query-data.json")
    query_result = qpystructs.get_value(result, query)
    assert query_result == {
        "WashingtonCities": "Bellevue, Olympia, Seattle"
    }
