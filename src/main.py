from fastapi import FastAPI
from controllers.all_routes import all_routes

app = FastAPI(
    debug=True,
    title="API Library",
    description="API for Library in FastAPI",
    version="0.1.5"
    )

all_routes(app)