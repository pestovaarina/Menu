from fastapi import FastAPI

from .database import Base, engine
from .routers import menu, submenu, dishes

BASE_PATH = "/api/v1"
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(menu.router, prefix=BASE_PATH)
app.include_router(submenu.router, prefix=BASE_PATH)
app.include_router(dishes.router, prefix=BASE_PATH)
