from fastapi import APIRouter
from Api.routers.models import *
from DataModels.ApiModels import ModelElements

router = APIRouter()


@router.get("/{id}/elements")
async def get_all_elements(model_id: str) -> ModelElements:
    await get_model(model_id)

    return archModelGraphDb.getElements(model_id)

async def get_visible_elements(model_id: str) -> ModelElements:
    pass