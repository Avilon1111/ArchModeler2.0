from starlette.testclient import TestClient

from Api.routers.models import *
from pydantic_core import from_json

from DataModels.ApiModels import Arrow, Block, ModelElements
from app import app

"""
interface:
get_visible_elements(model_id: str) -> ModelElements:
"""

client = TestClient(app)


def test_2_blocks_1_arrow():
    model = Model.model_validate(
        from_json('{"id": "test_create_read_update_delete_2", "name": "name_1", "author": "author", "info": "info"}'))
    client.post("/models", json=model.model_dump())

    block = Block.model_validate(from_json('{"id": "id_block_1", "name": "string", "info": "string",'
                                           '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                           '"type": "Context", "visibility": "visible"}'))

    client.post(f"/models/{model.id}/blocks", json=block.model_dump())
    block_2 = Block.model_validate(from_json('{"id": "id_block_2", "name": "zxc", "info": "stringzxc",'
                                             '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                             '"type": "Context", "visibility": "visible"}'))
    client.post(f"/models/{model.id}/blocks", json=block_2.model_dump())

    block_3 = Block.model_validate(from_json('{"id": "id_block_3", "name": "zxc", "info": "stringzxc",'
                                             '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                             '"type": "Context", "visibility": "invisible"}'))
    client.post(f"/models/{model.id}/blocks", json=block_3.model_dump())

    arrow = Arrow.model_validate(from_json('{"id": "","name": "string","info": "string",'
                                           '"from_element": "id_block_1","to_element": "id_block_2"}'))
    response = client.post(f"/models/{model.id}/arrows", json=arrow.model_dump())
    arrow.id = response.json()['id']

    arrow_2 = Arrow.model_validate(from_json('{"id": "","name": "string","info": "string",'
                                           '"from_element": "id_block_1","to_element": "id_block_3"}'))
    response = client.post(f"/models/{model.id}/arrows", json=arrow_2.model_dump())
    arrow_2.id = response.json()['id']
    try:

        response = client.get(f"/models/{model.id}/elements")

        assert response.status_code == 200

        assert block.model_dump() in response.json()['blocks']
        assert block_2.model_dump() in response.json()['blocks']
        assert block_3.model_dump() not in response.json()['blocks']

        assert arrow.model_dump() in response.json()['arrows']
        assert arrow_2.model_dump() not in response.json()['arrows']


    finally:
        client.delete(f"/models/{model.id}")
