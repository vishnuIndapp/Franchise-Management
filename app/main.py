from fastapi import FastAPI
from sqlalchemy import engine, text
from app.core.database import engine, Base
from app.models import user,franchise
import logging
from app.routes import auth,franchise,profile
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


logging.basicConfig(level=logging.INFO)



app = FastAPI(
    title="Franchise Management ",
    description="API for  Franchise system Management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def startup_event():
    try:
        # 🔹 Test DB Connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logging.info("✅ Database connected successfully")

        # 🔹 Create tables (optional for dev)
        Base.metadata.create_all(bind=engine)
        logging.info("✅ Tables checked/created")

    except Exception as e:
        logging.error(f"❌ Database connection failed: {str(e)}")
        raise e  # stop app if DB fails
    




@app.get("/")
def root():
    return {"message": "API Running 🚀"}


app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(franchise.router, prefix="/api/v1/franchise", tags=["franchise"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["profile"])