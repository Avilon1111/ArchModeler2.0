from starlette.testclient import TestClient

from Api.routers.models import *
from pydantic_core import from_json

from DataModels.ApiModels import Block
from app import app
"""
interface:
create_block(model_id: str, block: Block)
get_block(model_id: str, block_id: str)
change_block(model_id: str, block_id: str, block: Block)
delete_block(model_id: str, block_id: str)
"""
client = TestClient(app)


def test_create_read_update_delete():
    model = Model.model_validate(
        from_json('{"id": "test_create_read_update_delete_1", "name": "name_1", "author": "author", "info": "info"}'))
    client.post("/models", json=model.model_dump())

    try:
        block = Block.model_validate(from_json('{"name": "string", "info": "string",'
                                               '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                               '"type": "Context", "visibility": "visible"}'))
        block_2 = Block.model_validate(from_json('{"name": "zxc", "info": "stringzxc",'
                                                 '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                                 '"type": "Context", "visibility": "visible"}'))
        response = client.post(f"/models/{model.id}/blocks", json=block.model_dump())

        assert response.status_code == 200

        block_id = response.json()['id']

        block.id = block_id
        block_2.id = block_id


        response_2 = client.get(f"/models/{model.id}/blocks/{block_id}")

        assert response_2.status_code == 200
        assert response_2.json() == block.model_dump()

        response_3 = client.patch(f"/models/{model.id}/blocks", json=block_2.model_dump())

        assert response_3.status_code == 200
        assert response_3.json() == block_2.model_dump()

        response_4 = client.delete(f"/models/{model.id}/blocks/{block_id}")

        assert response_4.status_code == 200
    finally:
        client.delete(f"/models/{model.id}")



def test_read_non_existent():
    model = Model.model_validate(
        from_json('{"id": "test_read_non_existent", "name": "name_1", "author": "author", "info": "info"}'))
    client.post("/models", json=model.model_dump())
    try:
        block_id = 123
        response = client.get(f"/models/{model.id}/blocks/{block_id}")

        assert response.status_code == 404
        assert response.json() == {"detail": "Нет блока с данным id"}
    finally:
        client.delete(f"/models/{model.id}")
