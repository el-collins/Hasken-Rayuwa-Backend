import cloudinary
from core.config import settings
from fastapi import FastAPI, status
from routes.auth import auth_router
from routes.links import link_router
from routes.users import users_router
from routes.states import states_router
from routes.blogs import blog_router
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import logging


from db.database import start_engine

app = FastAPI(
    title=settings.TITLE,
    docs_url='/api/docs',
    description=settings.DESCRIPTION,
    version='/api/v1',
)

# Routers
app.include_router(link_router, prefix='/api/v1')
app.include_router(users_router, prefix='/api/v1')
app.include_router(states_router, prefix='/api/v1')
app.include_router(auth_router, prefix='/api/v1')
app.include_router(blog_router, prefix='/api/v1')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["*", "http://localhost:5173",],
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.on_event("startup")
def on_startup():
    # logger.info(f"Connecting to database: {settings.SQL_DATABASE_URI}")
    start_engine()


# @app.on_event("startup")
# def on_startup():
#     start_engine()


@app.get('/', include_in_schema=False, response_class=RedirectResponse, status_code=status.HTTP_302_FOUND)
def index():
    return '/api/docs'
