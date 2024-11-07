from fastapi.testclient import TestClient
from main import app
import sys
import os

# Add the project root to sys.path for module access
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

client = TestClient(app)

def test_add_sheep():
    # Set up the new sheep data
    new_sheep = {
        "id": 7,
        "name": "Luna",
        "breed": "Suffolk",
        "sex": "ewe"
    }

    # Send a POST request to add the new sheep
    response = client.post("/sheep/", json=new_sheep)

    # Check if the status code is 201 (created)
    assert response.status_code == 201

    # Check if the response matches the data we sent
    assert response.json() == new_sheep

    # Confirm the sheep was added by fetching it with a GET request
    get_response = client.get(f"/sheep/{new_sheep['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == new_sheep


def test_delete_sheep():
    # First, add a sheep to delete
    sheep_to_delete = {
        "id": 8,
        "name": "Daisy",
        "breed": "Merino",
        "sex": "ewe"
    }
    client.post("/sheep/", json=sheep_to_delete)

    # Delete the sheep
    response = client.delete(f"/sheep/{sheep_to_delete['id']}")
    assert response.status_code == 204

    # Confirm that the sheep was deleted
    get_response = client.get(f"/sheep/{sheep_to_delete['id']}")
    assert get_response.status_code == 404

def test_update_sheep():
    # Add a sheep to update
    sheep_to_update = {
        "id": 9,
        "name": "Benny",
        "breed": "Suffolk",
        "sex": "ram"
    }
    client.post("/sheep/", json=sheep_to_update)

    # Update the sheep's details
    updated_data = {
        "id": 9,
        "name": "Benny",
        "breed": "Texel",
        "sex": "ram"
    }
    response = client.put(f"/sheep/{sheep_to_update['id']}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

    # Confirm the update
    get_response = client.get(f"/sheep/{updated_data['id']}")
    assert get_response.status_code == 200
    assert get_response.json() == updated_data


def test_get_all_sheep():
    # Add a couple of sheep to the database
    sheep1 = {"id": 10, "name": "Molly", "breed": "Dorset", "sex": "ewe"}
    sheep2 = {"id": 11, "name": "Max", "breed": "Hampshire", "sex": "ram"}
    client.post("/sheep/", json=sheep1)
    client.post("/sheep/", json=sheep2)

    # Retrieve all sheep
    response = client.get("/sheep/")
    assert response.status_code == 200
    all_sheep = response.json()

    # Verify the sheep data
    assert any(sheep["id"] == sheep1["id"] for sheep in all_sheep)
    assert any(sheep["id"] == sheep2["id"] for sheep in all_sheep)
