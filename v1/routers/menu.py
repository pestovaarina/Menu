from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from .. import schemas
from ..dependencies import get_db
from ..crud import menu

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get(
    "",
    response_model=list[schemas.Menu],
    status_code=status.HTTP_200_OK,
    name='get_menus',
    description='Возвращает список всех меню.'
)
def get_menu_list(db: Session = Depends(get_db)):
    menu_list = menu.get_menu(db)
    return menu_list


@router.get(
    "/{menu_id}",
    response_model=schemas.Menu,
    status_code=status.HTTP_200_OK,
    name='get_menus_details',
    description='Возвращает меню с подменю и блюдами.'
)
def get_menu_detail(menu_id: str,
                    db: Session = Depends(get_db)) -> JSONResponse:
    menu_detail = menu.get_menu_by_id(db, menu_id)
    if not menu_detail:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "menu not found")
    return menu_detail


@router.post(
    "",
    response_model=schemas.Menu,
    status_code=status.HTTP_201_CREATED,
    name='create_menu',
    description='Создает новое меню.'
)
def create_menu(menu_data: schemas.CreateMenu = Body(...),
                db: Session = Depends(get_db)):
    new_menu = menu.create(db, menu_data)
    return new_menu


@router.patch(
        "/{menu_id}",
        response_model=schemas.Menu,
        status_code=status.HTTP_200_OK,
        name='update_menu',
        description='Обновляет меню новыми данными.'
)
def update_menu(menu_id: str, menu_data: schemas.CreateMenu,
                db: Session = Depends(get_db)):
    new_menu = menu.update(db, menu_id, menu_data)
    if not new_menu:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "menu not found")
    return new_menu


@router.delete(
        "/{menu_id}",
        response_model=schemas.InfoMessage,
        status_code=status.HTTP_200_OK,
        name='delete_menu',
        description='Удаляет меню.'
)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    menu.delete(db, menu_id)
    return schemas.InfoMessage(
        status=True, message="Меню удалено!"
    )
