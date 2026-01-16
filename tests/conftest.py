import sys
import os

# Add the project root (/code) to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture()
def client():
    return TestClient(app)