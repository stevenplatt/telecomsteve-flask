# example coverage report: python -m pytest --cov=application
# example verbose test: python -m pytest -v

import pytest
from application import application

@pytest.fixture
def client():
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client

def test_home_page(client):
    """Test that home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_about_page(client):
    """Test that about page loads successfully"""
    rv = client.get('/about')
    assert rv.status_code == 200

def test_contact_page(client):
    """Test that contact page loads successfully"""
    rv = client.get('/contact')
    assert rv.status_code == 200

def test_research_page(client):
    """Test that research page loads successfully"""
    rv = client.get('/research')
    assert rv.status_code == 200

def test_engineering_feeds(client):
    """Test that engineering feeds page loads successfully"""
    rv = client.get('/engineering')
    assert rv.status_code == 200