from starlette.testclient import TestClient

from Api.routers.models import *
from pydantic_core import from_json
from app import app

"""
create_model(model: Model), get_model(model_id: str), change_model(new_model: Model), delete_model(model_id: str)
"""
client = TestClient(app)


def test_create_read_update_delete():
    model = Model.model_validate(from_json('{"id": "test_create_read_update_delete_1", "name": "name_1", "author": "author", "info": "info"}'))
    model_2 = Model.model_validate(from_json('{"id": "test_create_read_update_delete_1", "name": "name_2", "author": "author", "info": "info"}'))

    response = client.post("/models", json=model.model_dump())

    assert response.status_code == 200
    assert response.json() == model.model_dump()

    response_2 = client.get(f"/models/{model.id}")

    assert response_2.status_code == 200
    assert response_2.json() == model.model_dump()

    response_3 = client.patch("/models", json=model_2.model_dump())

    assert response_3.status_code == 200
    assert response_3.json() == model_2.model_dump()

    response_4 = client.delete(f"/models/{model.id}")

    assert response_4.status_code == 200


def test_double_creation():
    model = Model.model_validate(from_json('{"id": "test_double_creation", "name": "name", "author": "author", "info": "info"}'))

    client.post("/models", json=model.model_dump())
    response = client.post("/models", json=model.model_dump())

    assert response.status_code == 208

    response = client.delete(f"/models/{model.id}")

    assert response.status_code == 200


def test_read_non_existent():
    id = "test_read_non_existent"

    response = client.get(f"/models/{id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Нет модели с данным id"}



