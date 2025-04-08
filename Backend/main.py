from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from Backend.config.db import engine
from Backend.models import user_model, blog_model
from Backend.api.v1_endpoints import otp, blog

load_dotenv()

# Create database tables
user_model.Base.metadata.create_all(bind=engine)
blog_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS (you can restrict origins later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(otp.router, prefix="/api/v1", tags=["Auth"])
app.include_router(blog.router, prefix="/api/v1", tags=["Blog"])
