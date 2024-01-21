from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas
from ..crud import dishes
from ..dependencies import get_db

router = APIRouter(
    prefix="/menus/{menu_id}/submenus/{submenu_id}/dishes", tags=["dishes"]
)


@router.get(
        "",
        response_model=list[schemas.Dish],
        status_code=status.HTTP_200_OK
)
def get_dish_list(submenu_id: str, db: Session = Depends(get_db)):
    dish_list = dishes.get_dishes(db, submenu_id)
    return dish_list


@router.get(
        "/{dish_id}",
        response_model=schemas.Dish,
        status_code=status.HTTP_200_OK
)
def get_dish(submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    dish = dishes.get_dishes_by_id(db, submenu_id, dish_id)
    if not dish:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "dish not found")
    return dish


@router.post(
        "",
        response_model=schemas.Dish,
        status_code=status.HTTP_201_CREATED
)
def create_dish(
    submenu_id: str,
    dish_data: schemas.CreateDish,
    db: Session = Depends(get_db)
):
    dish = dishes.create(db, submenu_id, dish_data)
    return dish


@router.patch(
        "/{dish_id}",
        response_model=schemas.Dish,
        status_code=status.HTTP_200_OK
)
def update_dish(
    submenu_id: str,
    dish_id: str,
    dish_data: schemas.CreateDish,
    db: Session = Depends(get_db)
):
    dish = dishes.update(db, submenu_id, dish_id, dish_data)
    if not dish:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "dish not found")
    return dish


@router.delete(
        "/{dish_id}",
        response_model=schemas.InfoMessage,
        status_code=status.HTTP_200_OK
)
def delete_dish(
    submenu_id: str, dish_id: str, db: Session = Depends(get_db)
):
    dishes.delete(db, submenu_id, dish_id)
    return schemas.InfoMessage(
        status=True, message="Блюдо удалено!")
