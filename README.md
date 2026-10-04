# 🎙️ NoticIAs Dúo: Generador Autónomo de Podcast Técnico con Sincronización a Spotify

Pipeline automatizado que investiga noticias reales de los últimos 7 días, redacta un guion en formato de **diálogo entre dos locutores (Jorge y Dalia)**, sintetiza las voces con **Edge-TTS (redes neuronales en español de México)**, ensambla el audio con **FFmpeg** y lo coloca automáticamente en la carpeta de **Archivos Locales de Spotify** para escucharlo en tu trayecto diario.

---

## 🎧 El Dúo de Locutores

- **Jorge (`es-MX-JorgeNeural`):** Voz masculina reflexiva, analítica y técnica. Se enfoca en arquitecturas, números, despliegues y buenas prácticas de ingeniería de datos.
- **Dalia (`es-MX-DaliaNeural`):** Voz femenina dinámica, entusiasta y curiosa. Aporta agilidad, cuestionamientos clave, casos de uso empresarial y las secciones de gadgets y cultura geek.

---

## 🗂️ Estructura del Proyecto

- [`podcast_synthesizer.py`](podcast_synthesizer.py): Motor central de síntesis TTS, limpieza fonética, ensamble con FFmpeg, etiquetado ID3 y generador de feed RSS.
- [`generate_daily_episode.py`](generate_daily_episode.py): Generador del episodio del día con investigación y guion estructurado en bloques temáticos.
- [`run_daily_podcast.bat`](run_daily_podcast.bat): Ejecutable por lotes para disparar la generación en un solo clic.
- [`schedule_podcast_task.ps1`](schedule_podcast_task.ps1): Script para programar la ejecución automática diaria en Windows Task Scheduler.
- `audio/`: Carpeta maestra con los MP3s generados y el archivo `podcast.xml` (RSS).
- `C:\Users\c_a_c\Music\NoticIAs\`: Carpeta sincronizada con Spotify.

---

## 📲 Configuración en Spotify (Paso a Paso)

### 1. Activar Archivos Locales en Spotify Desktop (Solo la primera vez)
1. Abre Spotify en tu computadora.
2. Haz clic en tu perfil (esquina superior derecha) y selecciona **Configuración**.
3. Baja hasta la sección **Archivos locales** y activa el interruptor **Mostrar archivos locales**.
4. Haz clic en **Añadir una fuente** y selecciona la carpeta:
   `C:\Users\c_a_c\Music\NoticIAs`
5. En el menú lateral izquierdo de Spotify, entra a **Tu biblioteca** -> **Archivos locales**.
6. Verás los episodios generados (ej. `NoticIAs Dúo: Gemini 3.8, Agentic BigQuery, Android 17 y Sword Art Online`).
7. Haz clic derecho sobre el episodio -> **Añadir a lista** -> Crea una lista llamada **`NoticIAs Diarias`**.

### 2. Sincronizar en el Celular para tu Trayecto
1. Abre Spotify en tu teléfono (asegúrate de estar conectado a la misma red Wi-Fi de tu casa/oficina que la PC).
2. Entra a la lista de reproducción **`NoticIAs Diarias`**.
3. Activa la opción **Descargar** (icono de la flecha hacia abajo).
4. El archivo se descargará a tu teléfono y estará listo para reproducirse en el coche o transporte sin gastar datos móviles.
