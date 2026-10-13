"""Clase base del Page Object Model.

Centraliza utilidades comunes a todas las páginas: navegación,
acceso a locators por data-testid y lectura de título.
Todas las páginas concretas heredan de BasePage.
"""
from __future__ import annotations

from playwright.sync_api import Locator, Page


class BasePage:
    """Base de todos los Page Objects."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navega a la URL indicada."""
        self.page.goto(url)

    def get_by_test_id(self, test_id: str) -> Locator:
        """Devuelve un locator por atributo data-testid.

        Mantener los locators detrás de este método hace que el POM
        dependa solo de data-testid y no de selectores frágiles.
        """
        return self.page.locator(f'[data-testid="{test_id}"]')

    @property
    def title(self) -> str:
        """Título (<title>) de la página actual."""
        return self.page.title()
