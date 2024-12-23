from fastapi import FastAPI
from Api.routers.elements import arrows, blocks, nests, elements
from Api.routers import models
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.include_router(elements.router)
app.include_router(nests.router)
app.include_router(blocks.router)
app.include_router(arrows.router)
app.include_router(models.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)