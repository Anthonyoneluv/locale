import pytest
import asyncio
import requests
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_get_regions(client):
    response = client.get("/regions/")
    assert response.status_code == 200
    assert len(response.json()) == 4  

def test_get_states(client):
    response = client.get("/states/")
    assert response.status_code == 200
    assert len(response.json()) == 3  
def test_get_lgas(client):
    response = client.get("/lgas/")
    assert response.status_code == 200
    assert len(response.json()) == 6  
    
@pytest.mark.asyncio
async def test_search(client):
    response = await client.get("/search/?query=Lagos")
    assert response.status_code == 200
    data = response.json()
    assert len(data['regions']) == 1
    assert len(data['states']) == 1
    assert len(data['lgas']) == 2

# Integration test to check if the API returns valid data
def test_api_returns_valid_data():
    response = requests.get("http://localhost:8000/regions/")
    assert response.status_code == 200
    regions = response.json()
    assert len(regions) == 4
    assert all('id' in region and 'name' in region for region in regions)

    response = requests.get("http://localhost:8000/states/")
    assert response.status_code == 200
    states = response.json()
    assert len(states) == 3
    assert all('id' in state and 'name' in state for state in states)

    response = requests.get("http://localhost:8000/lgas/")
    assert response.status_code == 200
    lgas = response.json()
    assert len(lgas) == 6
    assert all('id' in lga and 'name' in lga for lga in lgas)

    response = requests.get("http://localhost:8000/search/?query=Lagos")
    assert response.status_code == 200
    data = response.json()
    assert len(data['regions']) == 1
    assert len(data['states']) == 1
    assert len(data['lgas']) == 2
