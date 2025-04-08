from fastapi import FastAPI
from Backend.api.v1_endpoints import otp
from Backend.config.db import engine
from Backend.models import user_model
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()



# Create DB tables
user_model.Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()
app.include_router(otp.router, prefix="/api/v1", tags=["OTP"])
