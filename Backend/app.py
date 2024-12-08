from fastapi import FastAPI
from Api.routers.elements import arrows, blocks, nests
from Api.routers import models

app = FastAPI()



# app.include_router(elements.router)
app.include_router(nests.router)
app.include_router(blocks.router)
app.include_router(arrows.router)
app.include_router(models.router)