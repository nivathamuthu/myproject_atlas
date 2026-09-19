from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from atlas_api.file_upload import router as file_upload_router
from modules.auth.presentation.router import router as auth_router


app = FastAPI(
    title="Project Atlas API",
    version="0.1.0",
)


# CORS configuration for Atlas frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(file_upload_router)
app.include_router(auth_router)

