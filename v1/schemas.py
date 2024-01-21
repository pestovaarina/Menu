from pydantic import BaseModel


class InfoMessage(BaseModel):
    status: bool
    message: str


class CreateMenu(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class CreateMenuID(CreateMenu):
    id: str


class Menu(CreateMenuID):
    submenus_count: int
    dishes_count: int


class CreateSubmenu(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class CreateSubmenuID(CreateMenu):
    id: str


class Submenu(CreateSubmenuID):
    dishes_count: int


class CreateDish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        from_attributes = True


class CreateDishID(CreateDish):
    id: str
    price: float


class Dish(CreateDishID):
    price: str
