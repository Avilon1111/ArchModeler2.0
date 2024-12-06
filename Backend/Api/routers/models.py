from fastapi import APIRouter, HTTPException
from Database.database import archModelInfoDb, archModelGraphDb
from DataModels.ApiModels import Model
from DataModels.ModelsConvertor import ModelConvertor
router = APIRouter(prefix="/models", tags=["Модели"])

"""
Принимает API, возвращает API, к DB конвертирует
"""

@router.post("")
async def create_model(model: Model) -> Model:
    if archModelInfoDb.getModelDescription(model.model_id):
        raise HTTPException(status_code=208, detail="Модель c данным id уже создана")
    archModelGraphDb.createModel(ModelConvertor.convert_model_to_db(model))
    archModelInfoDb.createModel(ModelConvertor.convert_model_to_db(model))
    return model


@router.patch("")
async def change_model_description(model: Model) -> Model:
    db_model = archModelInfoDb.getModelDescription(model.model_id)
    if not db_model:
        raise HTTPException(status_code=404, detail="Модель не найдена")
    archModelInfoDb.changeModelDescription(ModelConvertor.convert_model_to_db(model))
    model = ModelConvertor.convert_model_to_api(archModelInfoDb.getModelDescription(model.model_id))
    return model


@router.delete("/{model_id}")
async def delete_model(model_id: str):
    model = archModelInfoDb.getModelDescription(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Модель не найдена")

    archModelInfoDb.deleteModel(model_id)
    archModelGraphDb.deleteModel(model_id)