import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROFILE_DIR = Path(r"C:\Carlos\noticias_podcast\browser_profile")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_AUDIO = Path(r"C:\Carlos\noticias_podcast\audio\NoticIAs_Duo_2026-10-03.mp3")
DEFAULT_TITLE = "#01 - Gemini 3.8 Flash, Agentic BigQuery, Android 17 y Sword Art Online"
DEFAULT_DESCRIPTION = """En este episodio de NoticIAs Dúo, Jorge y Dalia analizan las noticias tecnológicas más potentes de la semana:

• [0:00] Bienvenida e introducción al formato dúo.
• [0:35] IA & Google AI Studio: Cuotas diarias, Gemini 3.8 Flash con SynthID Bio y la transición oficial de Gems a Skills.
• [1:42] Data Engineering & Cloud: Agentic Data Cloud en BigQuery, MCP en dbt para VS Code y la regla de oro de orquestación con Apache Airflow.
• [3:10] Gadgets & Movilidad: Despliegue de One UI 9.0 (Android 17) para Samsung Galaxy S25 y firmware de Insta360 X4.
• [4:15] Geek & Anime: Tráiler de Demons' Crest de Reki Kawahara, nueva película de Sword Art Online y Mushoku Tensei T3.
• [5:00] Cierre y despedida."""

def main():
    print("\n" + "="*70)
    print("🚀 AUTOMATIZADOR DE SPOTIFY FOR CREATORS")
    print("="*70)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="msedge",
            headless=False,
            args=["--start-maximized"]
        )
        page = context.pages[0] if context.pages else context.new_page()

        print("Abriendo Spotify for Creators...")
        page.goto("https://creators.spotify.com/pod/dashboard", wait_until="domcontentloaded")
        
        # Give page 4 seconds to resolve any auth redirects
        time.sleep(4)

        # Check if login screen is present
        login_indicator = page.locator("text='¡Hola de nuevo!', text='Continuar con Google', text='Log in', input[type='email']")
        if login_indicator.count() > 0:
            print("\n" + "="*70)
            print("🔑 PANTALLA DE INICIO DE SESIÓN ACTIVA")
            print("La ventana permanecerá abierta hasta que inicies sesión.")
            print("Por favor selecciona tu método (Google, correo o contraseña).")
            print("="*70 + "\n")

            # Wait patiently until the login screen is no longer present
            while True:
                time.sleep(3)
                # Check if login elements are gone and we have creators dashboard
                has_login = page.locator("text='¡Hola de nuevo!', text='Continuar con Google', input[type='email']").count() > 0
                if not has_login:
                    time.sleep(3)
                    # Double check
                    if page.locator("text='¡Hola de nuevo!'").count() == 0:
                        print("¡Has iniciado sesión con éxito!")
                        break

        print("\nCargando tu panel de creador...")
        time.sleep(5)
        print(f"URL actual: {page.url}")
        page.screenshot(path=r"C:\Carlos\noticias_podcast\dashboard_screenshot.png")

        # Step 1: Click 'Nuevo episodio'
        print("Buscando botón 'Nuevo episodio'...")
        new_ep_btn = page.locator("button:has-text('Nuevo episodio'), button:has-text('New episode'), a:has-text('Nuevo episodio'), a:has-text('New episode'), [data-testid='new-episode-button']")
        
        if new_ep_btn.count() > 0 and new_ep_btn.first.is_visible():
            print("Haciendo clic en 'Nuevo episodio'...")
            new_ep_btn.first.click()
            time.sleep(4)
        else:
            print("Abriendo asistente de episodios...")
            page.goto("https://creators.spotify.com/pod/dashboard/episode/wizard")
            time.sleep(4)

        # Step 2: Upload audio file
        print("Buscando selector de archivo...")
        file_input = page.locator("input[type='file']")
        for _ in range(20):
            if file_input.count() > 0:
                break
            time.sleep(1)
            file_input = page.locator("input[type='file']")

        if file_input.count() > 0:
            print(f"Subiendo archivo de audio: {DEFAULT_AUDIO.name}...")
            file_input.first.set_input_files(str(DEFAULT_AUDIO))
            print("Audio inyectado exitosamente.")
            
            # Step 3: Wait for metadata inputs
            time.sleep(5)
            for _ in range(30):
                title_loc = page.locator("input[name='title'], input[placeholder*='título' i], input[placeholder*='title' i], input#title")
                if title_loc.count() > 0 and title_loc.first.is_visible():
                    print("Escribiendo título del episodio...")
                    title_loc.first.fill(DEFAULT_TITLE)
                    break
                time.sleep(2)

            desc_loc = page.locator("textarea[name='description'], textarea#description, div[contenteditable='true']")
            if desc_loc.count() > 0 and desc_loc.first.is_visible():
                print("Escribiendo notas del episodio y descripción...")
                try:
                    desc_loc.first.fill(DEFAULT_DESCRIPTION)
                except Exception:
                    desc_loc.first.click()
                    page.keyboard.insert_text(DEFAULT_DESCRIPTION)

            print("\n" + "="*70)
            print("🎉 ¡TODO CARGADO CON ÉXITO EN TU NAVEGADOR!")
            print("Audio cargado, título y descripción escritos.")
            print("Revisa la ventana del navegador y haz clic en 'Publicar ahora'.")
            print("="*70 + "\n")
            
            page.screenshot(path=r"C:\Carlos\noticias_podcast\upload_success.png")
            # Keep browser alive so user can review and publish
            time.sleep(120)
        else:
            print("No se encontró input[type='file']. Guardando captura de diagnóstico...")
            page.screenshot(path=r"C:\Carlos\noticias_podcast\debug_page.png")
            time.sleep(60)

if __name__ == '__main__':
    main()
