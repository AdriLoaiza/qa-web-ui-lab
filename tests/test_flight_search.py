"""Pruebas de la página de búsqueda de vuelos.

Validan el título de la página y el comportamiento del formulario,
usando el Page Object (POM) y reportando pasos a Allure.
"""
import allure
import pytest
from playwright.sync_api import Page, expect

from pages.flight_search_page import FlightSearchPage


@pytest.fixture
def flight_page(page: Page, flight_search_url: str) -> FlightSearchPage:
    """Abre la página de búsqueda de vuelos lista para interactuar."""
    fsp = FlightSearchPage(page)
    fsp.open(flight_search_url)
    return fsp


@allure.feature("Búsqueda de vuelos")
@allure.story("Carga de página")
@allure.severity(allure.severity_level.CRITICAL)
def test_page_title(flight_page: FlightSearchPage):
    """La página debe cargar con el título y encabezado correctos."""
    with allure.step("Validar el título del documento"):
        assert flight_page.title == "Buscador de Vuelos - QA Lab"

    with allure.step("Validar el encabezado visible"):
        expect(flight_page.heading).to_have_text("Buscador de Vuelos")


@allure.feature("Búsqueda de vuelos")
@allure.story("Comportamiento del formulario")
@allure.severity(allure.severity_level.NORMAL)
def test_search_with_valid_data(flight_page: FlightSearchPage):
    """Con origen y destino válidos, el formulario confirma la búsqueda."""
    with allure.step("Buscar vuelo Bogotá -> Madrid"):
        flight_page.search_flight("Bogotá", "Madrid")

    with allure.step("Validar mensaje de confirmación"):
        expect(flight_page.result).to_be_visible()
        assert "Bogotá" in flight_page.result_text()
        assert "Madrid" in flight_page.result_text()


@allure.feature("Búsqueda de vuelos")
@allure.story("Comportamiento del formulario")
@allure.severity(allure.severity_level.NORMAL)
def test_search_with_empty_fields_shows_error(flight_page: FlightSearchPage):
    """Enviar el formulario vacío debe mostrar un mensaje de error de negocio."""
    with allure.step("Enviar formulario sin completar campos"):
        flight_page.submit()

    with allure.step("Validar mensaje de error"):
        expect(flight_page.result).to_be_visible()
        assert "origen y destino" in flight_page.result_text().lower()
