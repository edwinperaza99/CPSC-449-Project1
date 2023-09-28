"""Main module to run server and serve endpoints for clients."""

import uvicorn
from asyncio import run
from uvicorn.server import Server
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from loguru import logger

import databases
import sqlalchemy

from .models import AvailableClassResponse
from .database_query import get_available_classes

app = FastAPI()
DATABASE_URL = "sqlite+aiosqlite:///./api/share/classes.db"
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get(path='/db_liveness', operation_id='check_db_health')
async def check_db_health():
    is_connected = database.is_connected
    logger.info(f'Database status:{is_connected}')
    if is_connected:        
        return JSONResponse(content= {'status': 'ok'}, status_code = status.HTTP_200_OK)
    else:
        return JSONResponse(content= {'status': 'not connected'}, status_code = status.HTTP_503_SERVICE_UNAVAILABLE)

@app.get(path="/classes", operation_id="available_classes", response_model = AvailableClassResponse)
async def available_classes(department_name: str):
    """API to fetch list of available classes for a given department name.

    Args:
        department_name (str): Department name

    Returns:
        AvailableClassResponse: AvailableClassResponse model
    """
    result = await get_available_classes(db=database, department_name=department_name)
    return AvailableClassResponse(available_classes = result)



async def main():
    """Start the server."""
    server = Server(uvicorn.Config(app=app, host="0.0.0.0", timeout_graceful_shutdown=30))
    await server.serve()

if __name__ == "__main__":
    run(main())

