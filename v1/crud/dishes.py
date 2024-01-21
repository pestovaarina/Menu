import uuid

from sqlalchemy.orm import Session

from .. import models, schemas


def get_dishes(db: Session, submenu_id: str):
    db_dishes_list = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id)
    dishes_list = []
    for dish in db_dishes_list:
        dish__repr = schemas.Dish(
            id=dish.id,
            title=dish.title,
            description=dish.description,
            price=f"{dish.price:.2f}"
        )
        dishes_list.append(dish__repr)
    return dishes_list


def get_dishes_by_id(db: Session, submenu_id: str, dish_id: str):
    db_dish = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id,
        models.Dish.id == dish_id).first()
    if db_dish:
        dish__repr = schemas.Dish(
            id=db_dish.id,
            title=db_dish.title,
            description=db_dish.description,
            price=f"{db_dish.price:.2f}"
        )
        return dish__repr
    return None


def create(db: Session, submenu_id: str, dish_data: schemas.CreateDish):
    dish_id = str(uuid.uuid4())
    dish = schemas.CreateDishID(
        id=dish_id,
        title=dish_data.title,
        description=dish_data.description,
        price=float(dish_data.price)
    )
    db_dish = models.Dish(**dish.model_dump(), submenu_id=submenu_id)
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    dish__repr = schemas.Dish(
        id=dish.id,
        title=dish.title,
        description=dish.description,
        price=f"{dish.price:.2f}"
    )
    return dish__repr


def update(db: Session, submenu_id: str, dish_id: str,
           dish_data: schemas.CreateDish):
    db_dish = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id,
        models.Dish.id == dish_id).first()
    if not db_dish:
        return None

    db_dish.title = dish_data.title
    db_dish.description = dish_data.description
    db_dish.price = float(dish_data.price)

    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)

    dish__repr = schemas.Dish(
        id=db_dish.id,
        title=db_dish.title,
        description=db_dish.description,
        price=f"{db_dish.price:.2f}"
    )
    return dish__repr


def delete(db: Session, submenu_id: str, dish_id: str):
    db_dish = db.query(models.Dish).filter(
        models.Dish.submenu_id == submenu_id,
        models.Dish.id == dish_id).first()
    if db_dish:
        db.delete(db_dish)
        db.commit()
