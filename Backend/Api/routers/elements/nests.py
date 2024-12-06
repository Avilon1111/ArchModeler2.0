from fastapi import APIRouter, HTTPException

from DataModels.ModelsConvertor import ModelConvertor
from Database.database import archModelGraphDb, archModelInfoDb
from DataModels.ApiModels import Nest
from arango.exceptions import DocumentInsertError, DocumentDeleteError

router = APIRouter(prefix="/models/{model_id}/nests", tags=["Model nests"])



@router.post("")
async def create_nest(model_id: str, nest: Nest):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.addNest(model_id, ModelConvertor.convert_nest_to_db(nest))
    except DocumentInsertError:
        raise HTTPException(status_code=404, detail="Элементы с данным id не найдены")


@router.delete("")
async def delete_nest(model_id: str, nest_id: str):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.deleteNest(model_id, nest_id)
    except DocumentDeleteError:
        raise HTTPException(status_code=404, detail="Элементы с данным id не найдены")


@router.patch("")
async def patch_arrow(model_id: str, nest_id: str, nest: Nest):
    await delete_nest(model_id, nest_id)
    await create_nest(model_id, nest)