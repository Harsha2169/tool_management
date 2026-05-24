from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routers import (
    tools,
    productions,
    performances,
    params,
    maintenances,
    lookups,
)

app = FastAPI(
    title="Tooling Master Records Management",
    description="API for managing industrial injection moulding tool records",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend Static Files
frontend_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend"
)

if os.path.isdir(frontend_dir):
    app.mount(
        "/ui",
        StaticFiles(directory=frontend_dir, html=True),
        name="frontend"
    )

# API Routers
app.include_router(tools.router)
app.include_router(productions.router)
app.include_router(performances.router)
app.include_router(params.router)
app.include_router(maintenances.router)
app.include_router(lookups.router)

# Root Endpoint
@app.get("/")
def root():
    return {
        "message": "Tooling Master Records Management API",
        "docs": "/docs",
        "ui": "/ui"
    }
