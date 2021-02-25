from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from mongoengine.connection import connect, disconnect
from starlette.exceptions import HTTPException as StarletteHTTPException

from base.baseMixin.generalMixin import base
from base.settings import DEBUG, API_URL
from base.view.userView import account_router

app = FastAPI(debug=DEBUG)
app.mount("/static", StaticFiles(directory="./base/static"), name="static")
app.include_router(account_router, prefix=base.route_prefix("user"), tags=["Account"])


@app.on_event("startup")
async def initialize_db():
    if connect(db="base"):
        print("database connected successfully")


@app.on_event("shutdown")
async def un_initialize_db():
    if disconnect():
        print("database connection failed")


@base.run_once
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/docs")


@base.run_once
@app.get(f"/", include_in_schema=False)
async def index():
    return RedirectResponse("/docs", status_code=status.HTTP_302_FOUND)
