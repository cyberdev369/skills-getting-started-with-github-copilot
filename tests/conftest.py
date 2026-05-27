import copy
import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
app_module = importlib.import_module("app")


@pytest.fixture
def client():
    # Arrange: snapshot current activities
    backup = copy.deepcopy(app_module.activities)
    client = TestClient(app_module.app)
    try:
        yield client
    finally:
        # Assert/Teardown: restore activities to original state
        app_module.activities.clear()
        app_module.activities.update(backup)
