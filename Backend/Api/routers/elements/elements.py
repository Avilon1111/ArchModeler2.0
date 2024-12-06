from DataModels.ApiModels import *
from fastapi import APIRouter, HTTPException
from Database.database import archModelGraphDb, archModelInfoDb

router = APIRouter(prefix="/models/{model_id}", tags=["Элементы модели"])

@router.get("/elements")
async def get_elements(model_id: str) -> ModelElements:
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    return archModelGraphDb.getElements(model_id)