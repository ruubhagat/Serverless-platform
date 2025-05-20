# # backend/app/main.py

# from fastapi import FastAPI
# from app.routers import functions
# from app.database import Base, engine

# Base.metadata.create_all(bind=engine)

# app = FastAPI(title="Serverless Function Platform")
# app.include_router(functions.router)
# backend/app/main.py

from fastapi import FastAPI
from app.routers import functions
from app.database import Base, engine
from app.utils.container_pool import initialize_pool  # 👈 Add this line

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Serverless Function Platform")
app.include_router(functions.router)

initialize_pool()  # 👈 Warm up the container pool on server startup
