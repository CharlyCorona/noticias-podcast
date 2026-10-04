import zipfile
import subprocess
import json
import re
import os
import unicodedata
from pathlib import Path
from datetime import datetime, timedelta

ZIP_PATH = Path(r"G:\Mi unidad\Takeout\takeout-20260927T173444Z-1-001.zip")
AUDIO_DIR = Path(r"C:\Carlos\noticias_podcast\audio")
SPOTIFY_DIR = Path(r"C:\Users\c_a_c\Music\NoticIAs")
TEMP_DIR = Path(r"C:\Carlos\noticias_podcast\temp")
RSS_FILE = AUDIO_DIR / "podcast.xml"
ROOT_RSS = Path(r"C:\Carlos\noticias_podcast\podcast.xml")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SPOTIFY_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# The 20 chapters from Takeout that were not previously uploaded to Spotify
EXCLUDED_ALREADY_ON_SPOTIFY = {
    "Gemini 30 versus ChatGPT la cita a ciegas.wav",
    "Gemini 3.0 gana prueba ciegas de lógica y velocidad.wav",
    "Google Flows a Fondo_ La Automatización de Workspace con IA y la Clave para Empezar (Starters y Gemini).wav",
    "Bases de Datos Vectoriales_ El Motor Oculto que Traduce el Caos del Mundo Real para ChatGPT y Gemini.wav",
    "Google Flows y Gemini_ La Automatización de Workspace que Entiende lo que Pides.wav",
    "NotebookLM el cerebro digital que sí razona.wav"
}

def clean_slug(text: str) -> str:
    # Normalize unicode
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Replace non-alphanumeric with underscores
    text = re.sub(r'[^a-zA-Z0-9]+', '_', text)
    return text.strip('_')[:60]

def get_clean_title(filename_base: str, metadata_json_bytes: bytes = None) -> str:
    if metadata_json_bytes:
        try:
            data = json.loads(metadata_json_bytes.decode('utf-8', errors='replace'))
            if data.get('title'):
                return data['title'].strip()
        except Exception:
            pass
    # fallback from filename
    title = filename_base.replace('_', ' ')
    return title.strip()

def process_all_20():
    print("=" * 60)
    print("Iniciando extracción y conversión de los 20 capítulos de sIA...")
    print("=" * 60)
    
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        all_wav_infos = [
            info for info in z.infolist() 
            if info.filename.startswith('Takeout/NotebookLM/sIA/Artifacts/') and info.filename.endswith('.wav')
        ]
        
        # Filter for the 20 episodes
        target_infos = []
        for info in all_wav_infos:
            base_name = info.filename.split('/')[-1]
            # Match excluding normalized
            is_excluded = False
            for exc in EXCLUDED_ALREADY_ON_SPOTIFY:
                if clean_slug(exc) == clean_slug(base_name):
                    is_excluded = True
                    break
            if not is_excluded:
                target_infos.append(info)

        print(f"Total capítulos a procesar: {len(target_infos)}")
        
        converted_episodes = []
        # Sort by filename
        target_infos = sorted(target_infos, key=lambda x: x.filename)
        
        # Base date for historical sequence: 2026-09-10 to 2026-09-29
        base_time = datetime(2026, 9, 10, 8, 0, 0)

        for idx, info in enumerate(target_infos, 1):
            base_name = info.filename.split('/')[-1][:-4]
            json_path = info.filename[:-4] + " metadata.json"
            meta_bytes = None
            if json_path in z.namelist():
                meta_bytes = z.read(json_path)
            
            clean_title = get_clean_title(base_name, meta_bytes)
            slug = clean_slug(clean_title)
            mp3_filename = f"sIA_Archivo_{idx:02d}_{slug}.mp3"
            mp3_path = AUDIO_DIR / mp3_filename
            spotify_path = SPOTIFY_DIR / mp3_filename
            
            print(f"\n[{idx}/{len(target_infos)}] Procesando: {clean_title}")
            
            # Extract WAV to temp
            temp_wav = TEMP_DIR / f"temp_{idx:02d}.wav"
            temp_wav.write_bytes(z.read(info.filename))
            
            # Convert to MP3
            cmd = [
                "ffmpeg", "-y",
                "-i", str(temp_wav),
                "-c:a", "libmp3lame",
                "-b:a", "96k",
                "-ar", "44100",
                "-metadata", f"title={clean_title}",
                "-metadata", "artist=Carlos Corona (sIA)",
                "-metadata", "album=sIA",
                "-metadata", "genre=Podcast",
                "-metadata", "date=2026",
                str(mp3_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Copy to Spotify local sync folder
            import shutil
            shutil.copy2(mp3_path, spotify_path)
            
            # Clean temp
            try:
                temp_wav.unlink()
            except Exception:
                pass
            
            file_size = mp3_path.stat().st_size
            ep_date = base_time + timedelta(days=idx, hours=idx % 3)
            
            converted_episodes.append({
                "title": f"sIA: {clean_title}",
                "filename": mp3_filename,
                "path": mp3_path,
                "size": file_size,
                "date": ep_date.strftime("%a, %d %b %Y %H:%M:%S GMT"),
                "description": f"Capítulo histórico de sIA: {clean_title}. Análisis e investigación sobre arquitectura de datos, IA generativa y estrategia digital por Carlos Corona."
            })
            print(f"  -> Generado: {mp3_filename} ({file_size / (1024*1024):.2f} MB)")

    # Now update RSS Feed
    print("\nActualizando feed RSS...")
    update_rss_with_all(converted_episodes)
    print("\n✅ ¡Todos los 20 capítulos convertidos e integrados con éxito!")

def update_rss_with_all(new_episodes):
    base_url = "https://charlycorona.github.io/noticias-podcast"
    cover_url = f"{base_url}/cover.jpg"
    
    # Read existing items
    existing_items = []
    existing_urls = set()
    if RSS_FILE.exists():
        content = RSS_FILE.read_text(encoding='utf-8')
        items = re.findall(r'<item>.*?</item>', content, re.DOTALL)
        for it in items:
            m = re.search(r'<enclosure\s+url="([^"]+)"', it)
            if m:
                existing_urls.add(m.group(1))
            existing_items.append(it.strip())

    # Build XML items for new episodes (sorted newest first)
    new_xml_items = []
    for ep in new_episodes:
        audio_url = f"{base_url}/audio/{ep['filename']}"
        if audio_url in existing_urls:
            continue
        
        item = f"""    <item>
      <title>{ep['title']}</title>
      <description>{ep['description']}</description>
      <pubDate>{ep['date']}</pubDate>
      <enclosure url="{audio_url}" length="{ep['size']}" type="audio/mpeg"/>
      <guid isPermaLink="true">{audio_url}</guid>
      <itunes:author>Carlos Corona (sIA)</itunes:author>
      <itunes:image href="{cover_url}"/>
      <itunes:explicit>no</itunes:explicit>
    </item>"""
        new_xml_items.append(item)

    # Put today's episodes first, then historical
    all_final_items = existing_items + new_xml_items
    items_block = "\n".join(all_final_items)

    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>sIA</title>
    <link>{base_url}</link>
    <language>es-mx</language>
    <itunes:author>Carlos Corona</itunes:author>
    <itunes:image href="{cover_url}"/>
    <itunes:category text="Technology"/>
    <itunes:owner>
      <itunes:name>Carlos Corona</itunes:name>
      <itunes:email>charly.corona@gmail.com</itunes:email>
    </itunes:owner>
    <description>sIA: El podcast de Inteligencia Artificial, Cloud, Big Data, Gadgets y Cultura Geek presentado por Carlos Corona, Jorge y Dalia.</description>
{items_block}
  </channel>
</rss>"""

    RSS_FILE.write_text(rss_content, encoding='utf-8')
    ROOT_RSS.write_text(rss_content, encoding='utf-8')
    print(f"Feed actualizado con un total de {len(all_final_items)} episodios.")

if __name__ == '__main__':
    process_all_20()
