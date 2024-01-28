from fastapi import status
from fastapi.testclient import TestClient
from ..v1.main import app


client = TestClient(app)


def test_create_menu(client, saved_data):
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
    """Добавление нового подменю."""
    submenu_data = {'title': 'Тестовое подменю',
                    'description': 'Тестовое подменю'}
    menu = saved_data['menu']
    response = client.post(f"/api/v1/menus/{menu['id']}/submenus",
                           json=submenu_data)
    assert response.status_code == status.HTTP_201_CREATED, \
        'Статус ответа не 201'
    assert 'id' in response.json(), 'Идентификатора подменю нет в ответе'
    assert 'title' in response.json(), 'Названия подменю нет в ответе'
    assert 'description' in response.json(), 'Описания подменю нет в ответе'
    assert 'dishes_count' in response.json(), 'Количества блюд нет в ответе'
    assert response.json()['dishes_count'] == 0
    assert response.json()['title'] == submenu_data['title'], \
        'Название подменю не соответствует ожидаемому'
    assert response.json()['description'] == submenu_data['description'], \
        'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = response.json()


def test_create_dish(saved_data):
    dish_data = {'title': 'Тестовое блюдо',
                 'description': 'Тестовое описание блюда', 'price': '27.50'}
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.post(f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes",
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
    saved_data['dish'] = data


def test_get_dish(saved_data):
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.get(f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/{dish['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert data['id'] == dish['id'], \
        'Идентификатор блюда не соответствует ожидаемому'
    assert data['title'] == dish['title'], \
        'Название блюда не соответствует ожидаемому'
    assert data['description'] == dish['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert data['price'] == dish['price'], \
        'Цена блюда не соответствует ожидаемой'


def test_update_dish(saved_data):
    dish_data = {'title': 'Обновленное название',
                 'description': 'Обновленное описание', 'price': '19.40'}
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.patch(f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/{dish['id']}",
                            json=dish_data)
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert 'id' in data, 'Идентификатора блюда нет в ответе'
    assert 'title' in data, 'Названия блюда нет в ответе'
    assert 'description' in data, 'Описания блюда нет в ответе'
    assert 'price' in data, 'Цены блюда нет в ответе'
    assert data['title'] == dish_data['title'], \
        'Название блюда не соответствует ожидаемому'
    assert data['description'] == dish_data['description'], \
        'Описание блюда не соответствует ожидаемому'
    assert data['price'] == dish_data['price'], \
        'Цена блюда не соответствует ожидаемой'
    saved_data['submenu'] = data


def test_delete_dish(saved_data):
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = client.delete(f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/{dish['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    response = client.get(f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}/dishes/{dish['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, \
        'Статус ответа не 404'
