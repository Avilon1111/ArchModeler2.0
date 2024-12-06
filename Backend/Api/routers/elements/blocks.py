from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException

from DataModels.ModelsConvertor import ModelConvertor
from Database.DbConnections import archModelInfoDb
from Database.database import archModelGraphDb
import arango

router = APIRouter(prefix="/models/{model_id}/blocks", tags=["Model blocks"])


@router.post("")
async def create_block(model_id: str, block: Block):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    archModelGraphDb.addBlock(model_id, ModelConvertor.convert_block_to_db(block))


@router.patch("")
async def patch_block(model_id: str, block_id: str, block: Block) -> Block:
    model = archModelGraphDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.changeBlock(model_id, block_id, ModelConvertor.convert_block_to_db(block))
        return ModelConvertor.convert_block_to_api(ModelConvertor.convert_model_to_db(block))
    except arango.exceptions.DocumentUpdateError:
        raise HTTPException(status_code=404, detail="Блок с данным id не найден")


@router.delete("")
async def delete_block(model_id: str, block_id: str):
    model = archModelGraphDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    try:
        archModelGraphDb.deleteBlock(model_id, block_id)
    except arango.exceptions.DocumentDeleteError:
        raise HTTPException(status_code=404, detail="Блок с данным id не найден")