from fastapi import APIRouter, HTTPException
from Database.database import archModelInfoDb, archModelGraphDb
from DataModels.ApiModels import Model
from DataModels.ModelsConvertor import ModelConvertor
import arango.exceptions

router = APIRouter(prefix="/models", tags=["Модели"])

@router.post("")
async def create_model(model: Model) -> Model:
    if archModelInfoDb.get_model(model.id):
        raise HTTPException(status_code=208, detail="Модель c данным id уже создана")

    try:
        archModelGraphDb.create_model(ModelConvertor.model_to_dict(model))
        archModelInfoDb.create_model(ModelConvertor.model_to_dict(model))
    except arango.exceptions.DocumentInsertError:
        raise HTTPException(status_code=500, detail="Не получилось создать модель")

    return await get_model(model.id)


@router.get("/{id}")
async def get_model(id: str) -> Model:
    try:
        model_dict = archModelInfoDb.get_model(id)
    except arango.exceptions.DocumentGetError:
        raise HTTPException(status_code=500, detail="Не получилось прочитать модель")

    if model_dict is None:
        raise HTTPException(status_code=404, detail="Нет модели с данным id")
    model = ModelConvertor.model_to_api(model_dict)

    return model


@router.patch("")
async def change_model(new_model: Model) -> Model:
    await get_model(new_model.id)

    try:
        archModelInfoDb.change_model(ModelConvertor.model_to_dict(new_model))
    except arango.exceptions.DocumentUpdateError:
        raise HTTPException(status_code=500, detail="Не получилось обновить модель")

    return await get_model(new_model.id)


@router.delete("/{id}")
async def delete_model(id: str) -> None:
    await get_model(id)
    try:
        archModelInfoDb.delete_model(id)
        archModelGraphDb.delete_model(id)
    except arango.exceptions.DocumentGetError:
        raise HTTPException(status_code=500, detail="Не получилось удалить модель")
