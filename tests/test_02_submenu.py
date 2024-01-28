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


def test_submenu_empty(saved_data):
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = client.get(f"/api/v1/menus/{menu['id']}/submenus")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_create_submenu(saved_data):
    """Добавление нового подменю."""
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
    assert data['title'] == submenu_data['title'], \
        'Название подменю не соответствует ожидаемому'
    assert data['description'] == submenu_data['description'], \
        'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = data


def test_get_submenu(saved_data):
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
    assert data['dishes_count'] == 0, \
        'Количество блюд не соответствует ожидаемому'


def test_update_submenu(saved_data):
    submenu_data = {'title': 'Обновленное название',
                    'description': 'Обновленное описание'}
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = client.patch(f"/api/v1/menus/{menu['id']}/"
                            f"submenus/{submenu['id']}",
                            json=submenu_data)
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert 'id' in data, 'Идентификатора подменю нет в ответе'
    assert 'title' in data, 'Названия подменю нет в ответе'
    assert 'description' in data, 'Описания подменю нет в ответе'
    assert 'dishes_count' in data, 'Количества блюд нет в ответе'
    assert data['title'] == submenu_data['title'], \
        'Название подменю не соответствует ожидаемому'
    assert data['description'] == submenu_data['description'], \
        'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = data


def test_delete_submenu(saved_data):
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
