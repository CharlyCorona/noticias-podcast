import urllib.request
import re
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

url = 'https://open.spotify.com/show/3oNxteAETV5wvEIPN1KDVN'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    # Check for ld+json
    ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for m in ld_matches:
        try:
            data = json.loads(m)
            print("LD+JSON Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except Exception:
            pass
            
    # Check for episode links
    episodes = re.findall(r'/episode/([a-zA-Z0-9]+)', html)
    unique_eps = list(dict.fromkeys(episodes))
    print(f"\nUnique Episode IDs found: {len(unique_eps)}")
    for e in unique_eps:
        print(f" - https://open.spotify.com/episode/{e}")

except Exception as ex:
    print(f"Error fetching show: {ex}")
