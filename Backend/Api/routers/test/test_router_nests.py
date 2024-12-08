from starlette.testclient import TestClient

from Api.routers.models import *
from pydantic_core import from_json

from DataModels.ApiModels import Nest, Block
from app import app
"""
interface:
create_nest(model_id: str, nest: Nest) -> Nest:
get_nest(model_id: str, nest_id: str) -> Nest:
change_nest(model_id: str, nest: Nest) -> Nest:
delete_nest(model_id: str, nest_id: str):
"""
client = TestClient(app)


def test_create_read_update_delete():
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
    try:

        nest = Nest.model_validate(from_json('{"id": "","name": "string","info": "string",'
                                               '"from_element": "id_block_1","to_element": "id_block_2","visibility": "visible"}'))
        nest_2 = Nest.model_validate(from_json('{"name": "string","info": "string",'
                                               '"from_element": "id_block_2","to_element": "id_block_1","visibility": "visible"}'))
        response = client.post(f"/models/{model.id}/nests", json=nest.model_dump())

        assert response.status_code == 200

        nest_id = response.json()['id']

        nest.id = nest_id
        nest_2.id = nest_id


        response_2 = client.get(f"/models/{model.id}/nests/{nest_id}")

        assert response_2.status_code == 200
        assert response_2.json() == nest.model_dump()

        response_3 = client.patch(f"/models/{model.id}/nests", json=nest_2.model_dump())

        assert response_3.status_code == 200
        assert response_3.json() == nest_2.model_dump()

        response_4 = client.delete(f"/models/{model.id}/nests/{nest_id}")

        assert response_4.status_code == 200
    finally:
        client.delete(f"/models/{model.id}")
        client.delete(f"/models/{model.id}/blocks/{block.id}")
        client.delete(f"/models/{model.id}/blocks/{block_2.id}")