from fastapi import status
from fastapi.testclient import TestClient
from ..v1.main import app


client = TestClient(app)


def test_create_menu(client, saved_data):
    """Создает меню."""

    menu_data = {'title': 'Тестовое меню', 'description': 'Тестовое описание'}
    response = client.post("/api/v1/menus", json=menu_data)
    assert response.status_code == status.HTTP_201_CREATED, \
        'Статус ответа не 201'
    data = response.json()
    assert data['title'] == menu_data['title'], \
        'Название меню не соответствует ожидаемому'
    assert data['description'] == menu_data['description'], \
        'Описание меню не соответствует ожидаемому'
    assert 'id' in data, 'Идентификатора меню нет в ответе'
    assert 'submenus_count' in data, \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in data, 'Количества блюд нет в ответе'
    saved_data['menu'] = data


def test_create_submenu(saved_data):
    """Создает подменю."""

    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}
    menu = saved_data['menu']
    response = client.post(f"/api/v1/menus/{menu['id']}/submenus",
                           json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED, \
        'Статус ответа не 201'
    data = response.json()
    assert 'id' in data, 'Идентификатора подменю нет в ответе'
    assert 'title' in data, 'Названия подменю нет в ответе'
    assert 'description' in data, 'Описания подменю нет в ответе'
    assert 'dishes_count' in data, 'Количества блюд нет в ответе'
    assert data['dishes_count'] == 0
    assert data['title'] == submenu_data['title'], \
        'Название подменю не соответствует ожидаемому'
    assert data['description'] == submenu_data['description'], \
        'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = data


def test_create_first_dish(saved_data):
    """Создает блюдо 1."""

    dish_data = {'title': 'Первое тестовое блюдо',
                 'description': 'Первое тестовое описание', 'price': '27.50'}
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(f"/api/v1/menus/{menu['id']}/"
                           f"submenus/{submenu['id']}/dishes",
                           json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED, \
        'Статус ответа не 201'
    data = response.json()
    assert 'id' in data, 'Идентификатора блюда нет в ответе'
    assert 'title' in data, 'Названия блюда нет в ответе'
    assert 'description' in data, 'Описания блюда нет в ответе'
    assert 'price' in data, 'Цены блюда нет в ответе'
    assert data['title'] == dish_data['title'], \
        'Название блюда не соответствует ожидаемому'
    assert data['description'] == dish_data['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert data['price'] == f"{float(dish_data['price']):.2f}", \
        'Цена блюда не соответствует ожидаемой'
    saved_data['dish_1'] = data


def test_create_second_dish(saved_data):
    """Создает блюдо 2."""

    dish_data = {'title': 'Второе тестовое блюдо',
                 'description': 'Второе тестовое описание', 'price': '267.590'}
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(f"/api/v1/menus/{menu['id']}/"
                           f"submenus/{submenu['id']}/dishes",
                           json=dish_data)
    assert response.status_code == status.HTTP_201_CREATED, \
        'Статус ответа не 201'
    data = response.json()
    assert 'id' in data, 'Идентификатора блюда нет в ответе'
    assert 'title' in data, 'Названия блюда нет в ответе'
    assert 'description' in data, 'Описания блюда нет в ответе'
    assert 'price' in data, 'Цены блюда нет в ответе'
    assert data['title'] == dish_data['title'], \
        'Название блюда не соответствует ожидаемому'
    assert data['description'] == dish_data['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert data['price'] == f"{float(dish_data['price']):.2f}", \
        'Цена блюда не соответствует ожидаемой'
    saved_data['dish_2'] = data


def test_get_menu(saved_data):
    """Просматривает определенное меню."""

    menu = saved_data['menu']
    response = client.get(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert data['title'] == menu['title']
    assert data['description'] == menu['description']
    assert data['id'] == str(menu['id'])
    assert data['submenus_count'] == 1
    assert data['dishes_count'] == 2


def test_get_submenu(saved_data):
    """Просматривает определенное подменю."""

    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(f"/api/v1/menus/{menu['id']}/"
                          f"submenus/{submenu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert data['id'] == submenu['id'], \
        'Идентификатор подменю не соответствует ожидаемому'
    assert data['title'] == submenu['title'], \
        'Название подменю не соответствует ожидаемому'
    assert data['description'] == submenu['description'], \
        'Описание подменю не соответствует ожидаемому'
    assert data['dishes_count'] == 2, \
        'Количество блюд не соответствует ожидаемому'


def test_delete_submenu(saved_data):
    """Удаляет подменю."""

    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.delete(f"/api/v1/menus/{menu['id']}/"
                             f"submenus/{submenu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    response = client.get(f"/api/v1/menus/{menu['id']}/"
                          f"submenus/{submenu['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, \
        'Статус ответа не 404'


def test_submenu_empty(saved_data):
    """Просматривает список подменю."""

    menu = saved_data['menu']
    response = client.get(f"/api/v1/menus/{menu['id']}/submenus")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_check_dishes_of_deleted_submenu(saved_data):
    """Просматривает список блюд."""

    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.get(f"/api/v1/menus/{menu['id']}/"
                          f"submenus/{submenu['id']}/dishes")
    dishes_after_deletion_submenu = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert dishes_after_deletion_submenu == [], 'В ответе непустой список'


def test_get_menu_after_del(saved_data):
    """Просматривает определенное меню."""

    menu = saved_data['menu']
    response = client.get(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert data['title'] == menu['title']
    assert data['description'] == menu['description']
    assert data['id'] == str(menu['id'])
    assert data['submenus_count'] == 0
    assert data['dishes_count'] == 0


def test_delete_menu(saved_data):
    """Удаляет меню."""

    menu = saved_data['menu']
    response = client.delete(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    response = client.get(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, \
        'Статус ответа не 404'


def test_all_menu_empty(client):
    """Просматривает список меню."""

    response = client.get("/api/v1/menus")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
