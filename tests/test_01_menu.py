from fastapi import status
from fastapi.testclient import TestClient
from ..v1.main import app


client = TestClient(app)


def test_all_menu_empty(client):
    """Проверка получения пустого списка меню."""
    response = client.get("/api/v1/menus")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


def test_create_menu(saved_data):
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


def test_get_menu(saved_data):
    menu = saved_data['menu']
    response = client.get(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert data['title'] == menu['title']
    assert data['description'] == menu['description']
    assert data['id'] == str(menu['id'])
    assert data['submenus_count'] == menu['submenus_count']
    assert data['dishes_count'] == menu['dishes_count']


def test_update_menu(saved_data):
    menu_data = {'title': 'Обновленное меню', 'description': 'Новое описание'}
    menu = saved_data['menu']
    response = client.patch(f"/api/v1/menus/{menu['id']}", json=menu_data)
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    data = response.json()
    assert 'id' in data, 'Идентификатора меню нет в ответе'
    assert 'title' in data, 'Названия меню нет в ответе'
    assert 'description' in data, 'Описания меню нет в ответе'
    assert 'submenus_count' in data, \
        'Количества подменю нет в ответе'
    assert 'dishes_count' in data, 'Количества блюд нет в ответе'
    assert data['title'] == menu_data['title'], \
        'Название меню не соответствует ожидаемому'
    assert data['description'] == menu_data['description'], \
        'Описание меню не соответствует ожидаемому'
    saved_data['menu'] = data


def test_delete_menu(saved_data):
    menu = saved_data['menu']
    response = client.delete(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_200_OK, \
        'Статус ответа не 200'
    response = client.get(f"/api/v1/menus/{menu['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, \
        'Статус ответа не 404'
