# -*- coding: utf-8 -*-
from cgbeacon2.server.auto import app
from cgbeacon2.instance import config_file_path


def test_auto(monkeypatch):
    """Test adding a WSGI middleware to the application"""

    monkeypatch.setenv("CGBEACON2_CONFIG", config_file_path, prepend=False)
    assert app.wsgi_app
