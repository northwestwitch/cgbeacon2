# -*- coding: utf-8 -*-
import pytest
from cgbeacon2.server import create_app

@pytest.fixture
def mock_app():
    app = create_app()
    return app
