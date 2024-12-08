from starlette.testclient import TestClient

from Api.routers.models import *
from pydantic_core import from_json

from DataModels.ApiModels import Arrow, Block
from app import app
"""
interface:
create_arrow(model_id: str, arrow: Arrow) -> Arrow:
get_arrow(model_id: str, arrow_id: str) -> Arrow:
change_arrow(model_id: str, arrow: Arrow) -> Arrow:
delete_arrow(model_id: str, arrow_id: str):
"""
client = TestClient(app)


def test_create_read_update_delete():
    model = Model.model_validate(
        from_json('{"id": "test_create_read_update_delete_2", "name": "name_1", "author": "author", "info": "info"}'))
    client.post("/models", json=model.model_dump())

    block = Block.model_validate(from_json('{"id": "id_block_1", "name": "string", "info": "string",'
                                           '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                           '"type": "Context"}'))

    client.post(f"/models/{model.id}/blocks", json=block.model_dump())
    block_2 = Block.model_validate(from_json('{"id": "id_block_2", "name": "zxc", "info": "stringzxc",'
                                             '"hit_box": {"width": 0,"height": 0,"x_axis": 0,"y_axis": 0,"rotation": 0},'
                                             '"type": "Context"}'))
    client.post(f"/models/{model.id}/blocks", json=block_2.model_dump())
    try:

        arrow = Arrow.model_validate(from_json('{"id": "","name": "string","info": "string",'
                                               '"from_element": "id_block_1","to_element": "id_block_2"}'))
        arrow_2 = Arrow.model_validate(from_json('{"name": "string","info": "string",'
                                               '"from_element": "id_block_2","to_element": "id_block_1"}'))
        response = client.post(f"/models/{model.id}/arrows", json=arrow.model_dump())

        assert response.status_code == 200

        arrow_id = response.json()['id']

        arrow.id = arrow_id
        arrow_2.id = arrow_id


        response_2 = client.get(f"/models/{model.id}/arrows/{arrow_id}")

        assert response_2.status_code == 200
        assert response_2.json() == arrow.model_dump()

        response_3 = client.patch(f"/models/{model.id}/arrows", json=arrow_2.model_dump())

        assert response_3.status_code == 200
        assert response_3.json() == arrow_2.model_dump()

        response_4 = client.delete(f"/models/{model.id}/arrows/{arrow_id}")

        assert response_4.status_code == 200
    finally:
        client.delete(f"/models/{model.id}")