import qpystructs
from data_constants import more_dict, more_json_dict
from qpystructs import operations


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
