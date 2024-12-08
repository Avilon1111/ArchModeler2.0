from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException
from Api.routers.models import get_model
from DataModels.ModelsConvertor import ModelConvertor
from Database.database import archModelGraphDb, archModelInfoDb
import arango

router = APIRouter(prefix="/models/{model_id}/nests", tags=["Model nests"])


@router.post("")
async def create_nest(model_id: str, nest: Nest) -> Nest:
    await get_model(model_id)
    try:
        archModelGraphDb.add_nest(model_id, ModelConvertor.nest_to_dict(nest))
    except arango.exceptions.DocumentInsertError:
        raise HTTPException(status_code=500, detail="Не получилось создать вложенность")

    return ModelConvertor.nest_to_api(archModelGraphDb.find_nest(model_id, ModelConvertor.nest_to_dict(nest)))

@router.get("/{nest_id}")
async def get_nest(model_id: str, nest_id: str) -> Nest:
    await get_model(model_id)

    try:
        nest_dict = archModelGraphDb.get_nest(model_id, nest_id)
    except arango.exceptions.DocumentGetError:
        raise HTTPException(status_code=500, detail="Не получилось прочитать вложенность")

    if nest_dict is None:
        raise HTTPException(status_code=404, detail="Нет вложенности с данным id")

    nest = ModelConvertor.nest_to_api(nest_dict)
    return nest


@router.patch("")
async def change_nest(model_id: str, nest: Nest) -> Nest:
    await get_model(model_id)
    await get_nest(model_id, nest.id)

    try:
        archModelGraphDb.change_nest(model_id, nest.id, ModelConvertor.nest_to_dict(nest))
    except arango.exceptions.DocumentUpdateError:
        raise HTTPException(status_code=404, detail="Вложенность с данным id не найдена")
    return await get_nest(model_id, nest.id)


@router.delete("/{nest_id}")
async def delete_nest(model_id: str, nest_id: str):
    await get_model(model_id)
    await get_nest(model_id, nest_id)

    try:
        archModelGraphDb.delete_nest(model_id, nest_id)
    except arango.exceptions.DocumentDeleteError:
        raise HTTPException(status_code=500, detail="Не получилось удалить вложеннлсть")