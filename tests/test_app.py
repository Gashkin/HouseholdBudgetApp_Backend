import pytest
from backend.app import app, db, Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_item(client):
    response = client.post('/api/items', json={
        'name': 'Milk',
        'category': 'Groceries',
        'amount': 2.5,
        'date': '2025-09-18',
        'notes': 'Organic',
        'paid': True
    })
    assert response.status_code == 201
    data = response.get_json()['item']
    assert data['name'] == 'Milk'
    assert data['paid'] is True

def test_get_items(client):
    client.post('/api/items', json={
        'name': 'Bread',
        'category': 'Groceries',
        'amount': 1.5,
        'date': '2025-09-17',
        'notes': '',
        'paid': False
    })
    response = client.get('/api/items')
    assert response.status_code == 200
    items = response.get_json()
    assert len(items) == 1
    assert items[0]['name'] == 'Bread'

def test_update_item(client):
    post_resp = client.post('/api/items', json={
        'name': 'Eggs',
        'category': 'Groceries',
        'amount': 3.0,
        'date': '2025-09-16',
        'notes': '',
        'paid': False
    })
    item_id = post_resp.get_json()['item']['id']
    put_resp = client.put(f'/api/items/{item_id}', json={
        'name': 'Eggs',
        'category': 'Groceries',
        'amount': 3.5,
        'date': '2025-09-16',
        'notes': 'Free range',
        'paid': True
    })
    assert put_resp.status_code == 200
    updated = put_resp.get_json()['item']
    assert updated['amount'] == 3.5
    assert updated['notes'] == 'Free range'
    assert updated['paid'] is True

def test_delete_item(client):
    post_resp = client.post('/api/items', json={
        'name': 'Butter',
        'category': 'Groceries',
        'amount': 4.0,
        'date': '2025-09-15',
        'notes': '',
        'paid': False
    })
    item_id = post_resp.get_json()['item']['id']
    del_resp = client.delete(f'/api/items/{item_id}')
    assert del_resp.status_code == 200
    deleted = del_resp.get_json()['item']
    assert deleted['name'] == 'Butter'
    # Ensure item is gone
    get_resp = client.get('/api/items')
    items = get_resp.get_json()
    assert all(i['id'] != item_id for i in items)
