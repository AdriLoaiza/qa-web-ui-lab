"""Page Object de la página de búsqueda de vuelos.

Encapsula los locators (solo data-testid) y los métodos de acción
de negocio. Los tests nunca tocan selectores directamente: siempre
pasan por los métodos de esta clase.
"""
from __future__ import annotations

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class FlightSearchPage(BasePage):
    """Representa la pantalla de búsqueda de vuelos."""

    # --- Identificadores data-testid (única fuente de verdad de los locators) ---
    HEADING = "page-heading"
    FORM = "flight-search-form"
    ORIGIN = "origin-input"
    DESTINATION = "destination-input"
    SEARCH_BUTTON = "search-button"
    RESULT = "search-result"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # --- Locators expuestos como propiedades ---
    @property
    def heading(self) -> Locator:
        return self.get_by_test_id(self.HEADING)

    @property
    def origin_input(self) -> Locator:
        return self.get_by_test_id(self.ORIGIN)

    @property
    def destination_input(self) -> Locator:
        return self.get_by_test_id(self.DESTINATION)

    @property
    def search_button(self) -> Locator:
        return self.get_by_test_id(self.SEARCH_BUTTON)

    @property
    def result(self) -> Locator:
        return self.get_by_test_id(self.RESULT)

    # --- Métodos de acción de negocio ---
    def open(self, url: str) -> "FlightSearchPage":
        """Abre la página de búsqueda de vuelos."""
        self.navigate(url)
        self.heading.wait_for(state="visible")
        return self

    def set_origin(self, origin: str) -> "FlightSearchPage":
        self.origin_input.fill(origin)
        return self

    def set_destination(self, destination: str) -> "FlightSearchPage":
        self.destination_input.fill(destination)
        return self

    def submit(self) -> "FlightSearchPage":
        """Pulsa el botón Buscar."""
        self.search_button.click()
        return self

    def search_flight(self, origin: str, destination: str) -> "FlightSearchPage":
        """Flujo completo de negocio: completar formulario y buscar."""
        self.set_origin(origin)
        self.set_destination(destination)
        self.submit()
        return self

    def result_text(self) -> str:
        """Texto del mensaje de resultado tras la búsqueda."""
        self.result.wait_for(state="visible")
        return self.result.inner_text()
