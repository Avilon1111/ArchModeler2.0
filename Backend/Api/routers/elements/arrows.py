from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException

from DataModels.ModelsConvertor import ModelConvertor
from Database.database import archModelGraphDb, archModelInfoDb
import arango

router = APIRouter(prefix="/models/{model_id}/arrows", tags=["Model arrows"])


@router.post("")
async def create_arrow(model_id: str, arrow: Arrow):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.addArrow(model_id, ModelConvertor.convert_arrow_to_db(arrow))
    except arango.exceptions.DocumentInsertError:
        raise HTTPException(status_code=404, detail="Элементы с данным id не найдены")

@router.delete("")
async def delete_arrow(model_id: str, arrow_id: str):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.deleteArrow(model_id, arrow_id)
    except arango.exceptions.DocumentDeleteError:
        raise HTTPException(status_code=404, detail="Элементы с данным id не найдены")

@router.patch("")
async def patch_arrow(model_id: str, arrow_id: str, arrow: Arrow) -> Arrow:
    await delete_arrow(model_id, arrow_id)
    await create_arrow(model_id, arrow)
