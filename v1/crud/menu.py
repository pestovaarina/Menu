import uuid

from sqlalchemy.orm import Session

from .. import schemas
from ..models import Menu


def get_menu(db: Session):
    db_menu_list = db.query(Menu).all()
    menu_list = []
    for menu in db_menu_list:
        submenu_count = len(menu.submenu)
        dishes_count = sum([len(sub.dishes) for sub in menu.submenu])
        menu_repr = schemas.Menu(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=submenu_count,
            dishes_count=dishes_count
        )
        menu_list.append(menu_repr)
    return menu_list


def get_menu_by_id(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        submenu_count = len(db_menu.submenu)
        dishes_count = sum([len(sub.dishes) for sub in db_menu.submenu])
        menu_repr = schemas.Menu(
            id=db_menu.id,
            title=db_menu.title,
            description=db_menu.description,
            submenus_count=submenu_count,
            dishes_count=dishes_count
        )
        return menu_repr
    return None


def create(db: Session, menu_data: schemas.CreateMenu):
    menu_id = str(uuid.uuid4())
    menu = schemas.CreateMenuID(
        id=menu_id,
        title=menu_data.title,
        description=menu_data.description
    )
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    menu_repr = schemas.Menu(
            id=menu_id,
            title=menu.title,
            description=menu.description,
            submenus_count=0,
            dishes_count=0
    )
    return menu_repr


def update(db: Session, menu_id: str, menu_data: schemas.CreateMenu):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        return None
    db_menu.title = menu_data.title
    db_menu.description = menu_data.description

    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    submenu_count = len(db_menu.submenu)
    dishes_count = sum([len(sub.dishes) for sub in db_menu.submenu])
    menu_repr = schemas.Menu(
            id=db_menu.id,
            title=db_menu.title,
            description=db_menu.description,
            submenus_count=submenu_count,
            dishes_count=dishes_count
    )
    return menu_repr


def delete(db: Session, menu_id: str):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if db_menu:
        db.delete(db_menu)
        db.commit()
