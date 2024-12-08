from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException

from DataModels.ModelsConvertor import ModelConvertor
from Database.database import archModelGraphDb
from Api.routers.models import get_model
import arango
import arango.exceptions

router = APIRouter(prefix="/models/{model_id}/blocks", tags=["Model blocks"])


@router.post("")
async def create_block(model_id: str, block: Block) -> Block:
    await get_model(model_id)
    try:
        archModelGraphDb.add_block(model_id, ModelConvertor.block_to_dict(block))
    except arango.exceptions.DocumentInsertError:
        raise HTTPException(status_code=500, detail="Не получилось создать блок")

    return ModelConvertor.block_to_api(archModelGraphDb.find_block(model_id, ModelConvertor.block_to_dict(block)))

@router.get("/{block_id}")
async def get_block(model_id: str, block_id: str) -> Block:
    await get_model(model_id)

    try:
        block_dict = archModelGraphDb.get_block(model_id, block_id)
    except arango.exceptions.DocumentGetError:
        raise HTTPException(status_code=500, detail="Не получилось прочитать блок")

    if block_dict is None:
        raise HTTPException(status_code=404, detail="Нет блока с данным id")

    block = ModelConvertor.block_to_api(block_dict)
    return block


@router.patch("")
async def change_block(model_id: str, block: Block) -> Block:
    await get_model(model_id)
    await get_block(model_id, block.id)

    try:
        archModelGraphDb.change_block(model_id, block.id, ModelConvertor.block_to_dict(block))
    except arango.exceptions.DocumentUpdateError:
        raise HTTPException(status_code=404, detail="Блок с данным id не найден")
    return await get_block(model_id, block.id)


@router.delete("/{block_id}")
async def delete_block(model_id: str, block_id: str):
    await get_model(model_id)
    await get_block(model_id, block_id)

    try:
        archModelGraphDb.delete_block(model_id, block_id)
    except arango.exceptions.DocumentDeleteError:
        raise HTTPException(status_code=500, detail="Не получилось удалить блок")