# -*- coding: utf-8 -*-
from cgbeacon2.server import create_app
from cgbeacon2.instance import config_file_path


def test_create_app_from_envar(monkeypatch):
    """Test option to create app from a file specified by an environment variable"""

    monkeypatch.setenv("CGBEACON2_CONFIG", config_file_path, prepend=False)
    assert create_app()
