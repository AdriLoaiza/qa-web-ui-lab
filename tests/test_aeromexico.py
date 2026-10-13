"""Pruebas sobre la página de Aeroméxico (ambiente dev).

Navegan a la URL remota https://dev.amlab7.com/new y validan:
  1. Que la página cargue, esperando >=3s para que se renderice la UI, y
     que exista el texto "Información del vuelo ABC de Aeroméxico.".
  2. Que exista el elemento con data-testid="home-header-nav-links".

Cada test reporta explícitamente a Allure si fue EXITOSO o FALLIDO,
adjuntando además una captura de pantalla como evidencia.
"""
import allure
import pytest
from playwright.sync_api import Page

AEROMEXICO_URL = "https://dev.amlab7.com/new"
EXPECTED_TEXT = "Información del vuelo ABC de Aeroméxico."
NAV_LINKS_TESTID = "home-header-nav-links"
UI_WAIT_MS = 3000  # espera mínima para que se visualice la UI


def _attach_screenshot(page: Page, name: str) -> None:
    """Adjunta una captura de pantalla al reporte de Allure."""
    allure.attach(
        page.screenshot(full_page=True),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def _abrir_aeromexico(page: Page):
    """Navega a la página y espera a que la UI de la SPA esté renderizada.

    Usamos 'domcontentloaded' (rápido y confiable) en lugar de 'networkidle',
    porque la página mantiene tráfico de red en segundo plano (analytics,
    sockets) que puede impedir que 'networkidle' se alcance nunca. Luego
    esperamos explícitamente al header de la SPA.
    """
    response = page.goto(AEROMEXICO_URL, wait_until="domcontentloaded", timeout=60000)
    assert response is not None, "No se recibió respuesta del servidor"
    assert response.ok, f"La página respondió con estado {response.status}"
    # Espera a que el header de la SPA se monte (señal fiable de UI lista).
    page.wait_for_selector('[data-testid="home-header"]', state="attached", timeout=30000)
    return response


def _cerrar_cookies_si_aparece(page: Page) -> None:
    """Cierra el banner de cookies si está presente; si no, no hace nada.

    El banner no siempre aparece, así que esto es best-effort: espera un
    tiempo corto por el botón "Aceptar" y, si no está visible, continúa
    sin fallar. Nunca interrumpe la validación posterior.
    """
    with allure.step("Cerrar banner de cookies si aparece"):
        aceptar = page.get_by_role("button", name="Aceptar", exact=True)
        try:
            # Espera breve: si el banner no aparece, seguimos sin fallar.
            aceptar.wait_for(state="visible", timeout=4000)
        except Exception:
            allure.attach(
                "El banner de cookies no apareció; no se requirió acción.",
                name="Cookies - no presente",
                attachment_type=allure.attachment_type.TEXT,
            )
            return

        aceptar.click()
        allure.attach(
            "El banner de cookies apareció y se cerró con 'Aceptar'.",
            name="Cookies - cerrado",
            attachment_type=allure.attachment_type.TEXT,
        )


@allure.feature("Aeroméxico")
@allure.story("Carga de página y texto de vuelo")
@allure.severity(allure.severity_level.CRITICAL)
def test_pagina_carga_y_muestra_texto_vuelo(page: Page):
    """La página carga y debe mostrar el texto de información del vuelo."""
    with allure.step(f"Navegar a {AEROMEXICO_URL}"):
        _abrir_aeromexico(page)

    with allure.step(f"Esperar {UI_WAIT_MS} ms a que se visualice la UI"):
        page.wait_for_timeout(UI_WAIT_MS)

    _cerrar_cookies_si_aparece(page)

    _attach_screenshot(page, "pagina-cargada")

    with allure.step(f"Buscar el texto: {EXPECTED_TEXT!r}"):
        # Comprobación determinista sobre el DOM ya renderizado (sin depender
        # del timing de los locators perezosos de Playwright).
        encontrado = EXPECTED_TEXT in page.inner_text("body")

    if encontrado:
        allure.attach(
            f"TEXTO ENCONTRADO: {EXPECTED_TEXT}",
            name="Resultado - EXITOSO",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("[EXITOSO] El texto fue encontrado en la página"):
            assert True
    else:
        allure.attach(
            f"TEXTO NO ENCONTRADO: {EXPECTED_TEXT}",
            name="Resultado - FALLIDO",
            attachment_type=allure.attachment_type.TEXT,
        )
        pytest.fail(
            f"[FALLIDO] El texto {EXPECTED_TEXT!r} no se encontró en la página."
        )


@allure.feature("Aeroméxico")
@allure.story("Barra de navegación del header")
@allure.severity(allure.severity_level.NORMAL)
def test_existe_data_testid_nav_links(page: Page):
    """Debe existir el elemento con data-testid=home-header-nav-links."""
    with allure.step(f"Navegar a {AEROMEXICO_URL}"):
        _abrir_aeromexico(page)

    with allure.step(f"Esperar {UI_WAIT_MS} ms a que se visualice la UI"):
        page.wait_for_timeout(UI_WAIT_MS)

    _cerrar_cookies_si_aparece(page)

    _attach_screenshot(page, "pagina-cargada")

    with allure.step(f"Buscar data-testid={NAV_LINKS_TESTID!r}"):
        encontrado = page.locator(f'[data-testid="{NAV_LINKS_TESTID}"]').count() > 0

    if encontrado:
        allure.attach(
            f"ELEMENTO ENCONTRADO: data-testid={NAV_LINKS_TESTID}",
            name="Resultado - EXITOSO",
            attachment_type=allure.attachment_type.TEXT,
        )
        with allure.step("[EXITOSO] El data-testid fue encontrado en la página"):
            assert True
    else:
        allure.attach(
            f"ELEMENTO NO ENCONTRADO: data-testid={NAV_LINKS_TESTID}",
            name="Resultado - FALLIDO",
            attachment_type=allure.attachment_type.TEXT,
        )
        pytest.fail(
            f"[FALLIDO] No se encontró el elemento data-testid={NAV_LINKS_TESTID!r}."
        )
