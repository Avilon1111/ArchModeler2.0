from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException
from Api.routers.models import get_model
from DataModels.ModelsConvertor import ModelConvertor
from Database.database import archModelGraphDb, archModelInfoDb
import arango

router = APIRouter(prefix="/models/{model_id}/arrows", tags=["Model arrows"])


@router.post("")
async def create_arrow(model_id: str, arrow: Arrow) -> Arrow:
    await get_model(model_id)
    try:
        archModelGraphDb.add_arrow(model_id, ModelConvertor.arrow_to_dict(arrow))
    except arango.exceptions.DocumentInsertError:
        raise HTTPException(status_code=500, detail="Не получилось создать стрелку")

    return ModelConvertor.arrow_to_api(archModelGraphDb.find_arrow(model_id, ModelConvertor.arrow_to_dict(arrow)))

@router.get("/{arrow_id}")
async def get_arrow(model_id: str, arrow_id: str) -> Arrow:
    await get_model(model_id)

    try:
        arrow_dict = archModelGraphDb.get_arrow(model_id, arrow_id)
    except arango.exceptions.DocumentGetError:
        raise HTTPException(status_code=500, detail="Не получилось прочитать стрелку")

    if arrow_dict is None:
        raise HTTPException(status_code=404, detail="Нет стрелки с данным id")

    arrow = ModelConvertor.arrow_to_api(arrow_dict)
    return arrow


@router.patch("")
async def change_arrow(model_id: str, arrow: Arrow) -> Arrow:
    await get_model(model_id)
    await get_arrow(model_id, arrow.id)

    try:
        archModelGraphDb.change_arrow(model_id, arrow.id, ModelConvertor.arrow_to_dict(arrow))
    except arango.exceptions.DocumentUpdateError:
        raise HTTPException(status_code=404, detail="Стрелка с данным id не найдена")
    return await get_arrow(model_id, arrow.id)


@router.delete("/{arrow_id}")
async def delete_arrow(model_id: str, arrow_id: str):
    await get_model(model_id)
    await get_arrow(model_id, arrow_id)

    try:
        archModelGraphDb.delete_arrow(model_id, arrow_id)
    except arango.exceptions.DocumentDeleteError:
        raise HTTPException(status_code=500, detail="Не получилось удалить стрелку")