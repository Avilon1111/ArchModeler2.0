from pydantic_core import from_json

from DataModels.ApiModels import *
from DataModels.ModelsConvertor import ModelConvertor


def test_model():
    model_dict: dict = {
        "_key": "key",
        "name": "name",
        "author": "author",
        "info": "info",
    }
    model_API = Model.model_validate(from_json('{"id": "key", "name": "name", "author": "author", "info": "info"}'))

    assert model_dict == ModelConvertor.model_to_dict(model_API)
    assert model_API == ModelConvertor.model_to_api(model_dict)

    assert model_dict == ModelConvertor.model_to_dict(ModelConvertor.model_to_api(model_dict))
    assert model_API == ModelConvertor.model_to_api(ModelConvertor.model_to_dict(model_API))


def test_block():
    block_dict: dict = {
        "_key": "id",
        "name": "name",
        "info": "info",
        "hit_box": {
            "width": 12,
            "height": 12,
            "x_axis": 15,
            "y_axis": 15,
            "rotation": 0
        },
        "type": "Context",
        "visibility": Visibility.visible
    }

    block_API = Block.model_validate(from_json(
        '{"id": "id", "name": "name", "info": "info","hit_box": {"width": 12, "height": 12, "x_axis": 15, "y_axis": 15, "rotation": 0}, "type": "Context", "visibility": "visible"}'))

    assert block_dict == ModelConvertor.block_to_dict(block_API)
    assert block_API == ModelConvertor.block_to_api(block_dict)

    assert block_dict == ModelConvertor.block_to_dict(ModelConvertor.block_to_api(block_dict))
    assert block_API == ModelConvertor.block_to_api(ModelConvertor.block_to_dict(block_API))


def test_block_no_id():
    block_dict: dict = {
        "name": "name",
        "info": "info",
        "hit_box": {
            "width": 12,
            "height": 12,
            "x_axis": 15,
            "y_axis": 15,
            "rotation": 0
        },
        "type": "Context",
        "visibility": Visibility.visible
    }

    block_API = Block.model_validate(from_json(
        '{"name": "name", "info": "info","hit_box": {"width": 12, "height": 12, "x_axis": 15, "y_axis": 15, "rotation": 0}, "type": "Context", "visibility": "visible"}'))

    assert block_dict == ModelConvertor.block_to_dict(block_API)
    assert block_API == ModelConvertor.block_to_api(block_dict)

    assert block_dict == ModelConvertor.block_to_dict(ModelConvertor.block_to_api(block_dict))
    assert block_API == ModelConvertor.block_to_api(ModelConvertor.block_to_dict(block_API))


def test_arrow():
    arrow_dict: dict = {
        "_key": "id",
        "name": "string",
        "info": "string",
        "_from": "arrows/string",
        "_to": "arrows/string",
        "visibility": "visible"
    }

    arrow_API = Arrow.model_validate(from_json(
        '{"id": "id", "name": "string", "from_element": "string", "to_element": "string", "visibility": "visible", "info": "string"}'))

    assert arrow_dict == ModelConvertor.arrow_to_dict(arrow_API)
    assert arrow_API == ModelConvertor.arrow_to_api(arrow_dict)

    assert arrow_dict == ModelConvertor.arrow_to_dict(ModelConvertor.arrow_to_api(arrow_dict))
    assert arrow_API == ModelConvertor.arrow_to_api(ModelConvertor.arrow_to_dict(arrow_API))

def test_arrow_no_id():
    arrow_dict: dict = {
        "name": "string",
        "info": "string",
        "_from": "arrows/string",
        "_to": "arrows/string",
        "visibility": "visible"
    }

    arrow_API = Arrow.model_validate(from_json(
        '{"name": "string", "from_element": "string", "to_element": "string", "visibility": "visible", "info": "string"}'))

    assert arrow_dict == ModelConvertor.arrow_to_dict(arrow_API)
    assert arrow_API == ModelConvertor.arrow_to_api(arrow_dict)

    assert arrow_dict == ModelConvertor.arrow_to_dict(ModelConvertor.arrow_to_api(arrow_dict))
    assert arrow_API == ModelConvertor.arrow_to_api(ModelConvertor.arrow_to_dict(arrow_API))

def test_nest():
    nest_dict: dict = {
        "_key": "id",
        "name": "string",
        "info": "string",
        "_from": "nests/string",
        "_to": "nests/string",
    }

    nest_API = Nest.model_validate(from_json(
        '{"id": "id", "name": "string", "from_element": "string", "to_element": "string", "info": "string"}'))

    assert nest_dict == ModelConvertor.nest_to_dict(nest_API)
    assert nest_API == ModelConvertor.nest_to_api(nest_dict)

    assert nest_dict == ModelConvertor.nest_to_dict(ModelConvertor.nest_to_api(nest_dict))
    assert nest_API == ModelConvertor.nest_to_api(ModelConvertor.nest_to_dict(nest_API))

def test_nest_no_id():
    nest_dict: dict = {
        "name": "string",
        "info": "string",
        "_from": "nests/string",
        "_to": "nests/string",
    }

    nest_API = Nest.model_validate(from_json(
        '{"name": "string", "from_element": "string", "to_element": "string", "info": "string"}'))

    assert nest_dict == ModelConvertor.nest_to_dict(nest_API)
    assert nest_API == ModelConvertor.nest_to_api(nest_dict)

    assert nest_dict == ModelConvertor.nest_to_dict(ModelConvertor.nest_to_api(nest_dict))
    assert nest_API == ModelConvertor.nest_to_api(ModelConvertor.nest_to_dict(nest_API))
