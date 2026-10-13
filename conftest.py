"""Fixtures compartidas para el proyecto QA Web UI.

Expone la URL de la página local de búsqueda de vuelos y configura
el navegador en modo headless por defecto.
"""
from pathlib import Path

import pytest

# Ruta absoluta a la página HTML local servida vía file://
APP_DIR = Path(__file__).parent / "app"
FLIGHT_SEARCH_URL = (APP_DIR / "flight-search.html").resolve().as_uri()


@pytest.fixture(scope="session")
def flight_search_url() -> str:
    """URL file:// de la página de búsqueda de vuelos."""
    return FLIGHT_SEARCH_URL


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, pytestconfig):
    """Por defecto corre headless; respeta --headed si se pasa en la CLI.

    pytest-playwright expone la opción --headed. Solo forzamos headless
    cuando el usuario NO pidió explícitamente modo headed, de modo que
    `pytest ... --headed` sí abra el navegador visible.
    """
    headed = pytestconfig.getoption("--headed", default=False)
    return {**browser_type_launch_args, "headless": not headed}
