from fastapi import APIRouter
from DataModels.DbModels import *
from Api.routers.models import *
from DataModels.ApiModels import ModelElements
from DataModels.Statuses import Visibility

router = APIRouter()


@router.get("/models/{model_id}/elements")
async def get_visible_elements(model_id: str) -> ModelElements:
    await get_model(model_id)

    elements_dict = archModelGraphDb.get_visible_elements(model_id)
    elements_api = ModelElements()

    for block in elements_dict[CollectionNames.blocks.name]:
        block_api = ModelConvertor.block_to_api(block)
        elements_api.blocks.insert(0, block_api)

    for arrow in elements_dict[CollectionNames.arrows.name]:
        arrow_api = ModelConvertor.arrow_to_api(arrow)
        elements_api.arrows.insert(0, arrow_api)

    return elements_api
