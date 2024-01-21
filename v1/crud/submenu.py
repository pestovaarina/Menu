import uuid

from sqlalchemy.orm import Session

from .. import models, schemas


def get_submenu(db: Session, menu_id: str):
    db_submenu_list = db.query(models.Submenu).filter(
        models.Submenu.menu_id == menu_id)
    submenu_list = []
    for submenu in db_submenu_list:
        dishes_count = len(submenu.dishes)
        submenu_repr = schemas.Submenu(
            id=submenu.id,
            title=submenu.title,
            description=submenu.description,
            dishes_count=dishes_count
        )
        submenu_list.append(submenu_repr)
    return submenu_list


def get_submenu_by_id(db: Session, menu_id: str, submenu_id: str):
    db_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id).first()
    if db_submenu:
        dishes_count = len(db_submenu.dishes)
        submenu_repr = schemas.Submenu(
            id=db_submenu.id,
            title=db_submenu.title,
            description=db_submenu.description,
            dishes_count=dishes_count
        )
        return submenu_repr
    return None


def create(db: Session, menu_id: str, submenu_data: schemas.CreateSubmenu):
    submenu_id = str(uuid.uuid4())
    submenu = schemas.CreateSubmenuID(
        id=submenu_id,
        title=submenu_data.title,
        description=submenu_data.description
    )
    db_submenu = models.Submenu(**submenu.model_dump(), menu_id=menu_id)
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    submenu_repr = schemas.Submenu(
        id=submenu.id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=0
    )
    return submenu_repr


def update(db: Session, menu_id: str, submenu_id: str,
           submenu_data: schemas.CreateSubmenu):
    db_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id
    ).first()
    if not db_submenu:
        return None

    db_submenu.title = submenu_data.title
    db_submenu.description = submenu_data.description

    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)

    dishes_count = len(db_submenu.dishes)
    submenu_dto = schemas.Submenu(
        id=db_submenu.id,
        title=db_submenu.title,
        description=db_submenu.description,
        dishes_count=dishes_count
    )
    return submenu_dto


def delete(db: Session, menu_id: str, submenu_id: str):
    db_submenu = db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id,
        models.Submenu.menu_id == menu_id
    ).first()
    if db_submenu:
        db.delete(db_submenu)
        db.commit()
