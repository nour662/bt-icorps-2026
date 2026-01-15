import pytest
from fastapi.testclient import testclient
from app.main import app

@pytest.fixture()
def client():
    return TestClient(app)