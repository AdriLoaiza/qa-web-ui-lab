"""Prueba que abre la página de Aeroméxico (ambiente dev).

A diferencia del resto del lab (que corre contra una página HTML local),
este test navega a la URL remota https://dev.amlab7.com/new y valida:
  1. Que la página cargue correctamente.
  2. Que exista el texto "Información del vuelo ABC de Aeroméxico.".
  3. Que exista el elemento con data-testid="home-sp01-benefits-title".
"""
import allure
import pytest
from playwright.sync_api import Page, expect

AEROMEXICO_URL = "https://dev.amlab7.com/new"
EXPECTED_TEXT = "Información del vuelo ABC de Aeroméxico."
BENEFITS_TITLE_TESTID = "home-sp01-benefits-title"


@allure.feature("Aeroméxico")
@allure.story("Apertura de página")
@allure.severity(allure.severity_level.CRITICAL)
def test_open_aeromexico_page(page: Page):
    """Abre la página de Aeroméxico y valida carga, texto y data-testid."""
    with allure.step(f"Navegar a {AEROMEXICO_URL}"):
        response = page.goto(AEROMEXICO_URL, wait_until="networkidle", timeout=60000)

    with allure.step("Validar que la respuesta HTTP sea exitosa"):
        assert response is not None, "No se recibió respuesta del servidor"
        assert response.ok, f"La página respondió con estado {response.status}"

    with allure.step(f"Validar que exista el texto: {EXPECTED_TEXT!r}"):
        expect(page.get_by_text(EXPECTED_TEXT)).to_be_visible()

    with allure.step(f"Validar que exista data-testid={BENEFITS_TITLE_TESTID!r}"):
        expect(page.get_by_test_id(BENEFITS_TITLE_TESTID)).to_be_visible()
