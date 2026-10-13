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
def browser_type_launch_args(browser_type_launch_args):
    """Fuerza modo headless (sobre-escribible con --headed en CLI)."""
    return {**browser_type_launch_args, "headless": True}
