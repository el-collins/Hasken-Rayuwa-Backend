import os
import cloudinary
from core.config import settings
from fastapi import FastAPI, status
from routes.auth import auth_router
from routes.links import link_router
from routes.users import users_router
from routes.states import states_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from db.database import start_engine

app = FastAPI(
    title=settings.TITLE,
    docs_url=settings.DOCS_URL,
    description=settings.DESCRIPTION,
    version=settings.API_VERSION
)

# Routers
app.include_router(link_router, prefix=settings.API_VERSION)
app.include_router(users_router, prefix=settings.API_VERSION)
app.include_router(states_router, prefix=settings.API_VERSION)
app.include_router(auth_router, prefix=settings.API_VERSION)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization"],
)

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)

@app.on_event("startup")
def on_startup():
    start_engine()

@app.get('/', include_in_schema=False, response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
def index():
    return settings.DOCS_URL
