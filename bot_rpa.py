# bot_rpa.py - Moteur RPA Cloud adapté sans écran physique
from playwright.sync_api import sync_playwright
import time
import os

def start_cloud_autofill(service_cfg, client_data):
    """
    Lance le robot en mode serveur, remplit le formulaire 
    et extrait une capture du CAPTCHA pour l'afficher sur le web.
    """
    p = sync_playwright().start()
    browser = p.chromium.launch(
        headless=True,  # Mode Cloud sans écran physique
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()

    try:
        print(f"[RPA Cloud] Navigation vers : {service_cfg['url']}")
        page.goto(service_cfg["url"], timeout=45000, wait_until="networkidle")
        time.sleep(1.5)

        # 1. Remplissage automatique des champs
        champs_map = service_cfg.get("champs", {})
        remplis = 0

        for cle, selecteurs in champs_map.items():
            valeur = client_data.get(cle, "")
            if not valeur:
                continue

            for selector in selecteurs:
                try:
                    element = page.locator(selector).first
                    if element.is_visible(timeout=1000):
                        element.fill(str(valeur))
                        remplis += 1
                        break
                except Exception:
                    continue

        # 2. Capture d'écran de la zone de contrôle (Human-in-the-Loop)
        captcha_path = "captcha_screenshot.png"
        page.screenshot(path=captcha_path, full_page=False)

        return {
            "status": "WAITING_HUMAN_VALIDATION",
            "filled_fields": remplis,
            "captcha_image": captcha_path,
            "playwright_session": {
                "playwright": p,
                "browser": browser,
                "page": page
            }
        }

    except Exception as e:
        browser.close()
        p.stop()
        return {"status": "ERROR", "message": str(e)}

def submit_with_captcha(session_data, captcha_code):
    """
    Injecte le code résolu par le Kâtib et récupère le reçu officiel.
    """
    page = session_data["page"]
    browser = session_data["browser"]
    p = session_data["playwright"]

    try:
        # Tente de trouver le champ du code de vérification / CAPTCHA
        captcha_selectors = ["#captcha", "#code_verification", "input[name*='captcha']", "input[placeholder*='code']"]
        for s in captcha_selectors:
            try:
                el = page.locator(s).first
                if el.is_visible(timeout=1000):
                    el.fill(str(captcha_code))
                    break
            except Exception:
                continue

        # Capture finale du récépissé
        time.sleep(2)
        receipt_path = "recu_officiel.png"
        page.screenshot(path=receipt_path, full_page=True)

        browser.close()
        p.stop()
        return {"status": "SUCCESS", "receipt": receipt_path}

    except Exception as e:
        browser.close()
        p.stop()
        return {"status": "ERROR", "message": str(e)}