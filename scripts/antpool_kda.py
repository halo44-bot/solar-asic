#!/usr/bin/env python3
"""
Antpool KDA API — Récupère les stats du compte KDA via signature HMAC-SHA256.
Lancé par le sensor command_line de Home Assistant toutes les 10 minutes.
Sortie : JSON sur stdout contenant les attributs Antpool.

═══ Lecture des credentials ═══
Le script lit les credentials dans cet ordre de priorité :
  1. Variables d'environnement (ANTPOOL_USER_ID, ANTPOOL_API_KEY, ANTPOOL_API_SECRET)
  2. Fichier /config/secrets.yaml de HA (clés antpool_user_id / antpool_api_key / antpool_api_secret)
  3. Fichier /config/www/secrets.js (mêmes noms de constantes que dans le dashboard)

═══ Installation ═══
  1. Placer ce fichier dans /config/scripts/antpool_kda.py
  2. chmod +x /config/scripts/antpool_kda.py
  3. Renseigner les credentials selon UNE des 3 méthodes ci-dessus
  4. Ajouter le sensor command_line dans configuration.yaml
"""
import hmac
import hashlib
import time
import json
import sys
import os
import re
import urllib.request
import urllib.parse


def load_credentials():
    """Lit USER_ID, API_KEY, API_SECRET selon 3 méthodes par ordre de priorité."""
    user_id    = os.environ.get("ANTPOOL_USER_ID", "")
    api_key    = os.environ.get("ANTPOOL_API_KEY", "")
    api_secret = os.environ.get("ANTPOOL_API_SECRET", "")
    coin       = os.environ.get("ANTPOOL_COIN", "KDA")

    if user_id and api_key and api_secret:
        return user_id, api_key, api_secret, coin

    # Méthode 2 : /config/secrets.yaml de HA (parsing manuel sans PyYAML)
    for path in ("/config/secrets.yaml", "/homeassistant/secrets.yaml"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                for key, var in (("antpool_user_id", "user_id"),
                                 ("antpool_api_key", "api_key"),
                                 ("antpool_api_secret", "api_secret"),
                                 ("antpool_coin", "coin")):
                    m = re.search(rf'^{key}\s*:\s*["\']?([^"\'\n#]+)["\']?',
                                  content, re.MULTILINE)
                    if m:
                        val = m.group(1).strip()
                        if var == "user_id":    user_id    = val
                        elif var == "api_key":   api_key    = val
                        elif var == "api_secret": api_secret = val
                        elif var == "coin":      coin       = val
                if user_id and api_key and api_secret:
                    return user_id, api_key, api_secret, coin
            except Exception:
                pass

    # Méthode 3 : /config/www/secrets.js (regex sur les const ANTPOOL_*)
    for path in ("/config/www/secrets.js", "/homeassistant/www/secrets.js"):
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                patterns = {
                    "user_id":    r'(?:const|let|var)\s+ANTPOOL_USER_ID\s*=\s*["\']([^"\']+)["\']',
                    "api_key":    r'(?:const|let|var)\s+ANTPOOL_API_KEY\s*=\s*["\']([^"\']+)["\']',
                    "api_secret": r'(?:const|let|var)\s+ANTPOOL_API_SECRET\s*=\s*["\']([^"\']+)["\']',
                    "coin":       r'(?:const|let|var)\s+ANTPOOL_COIN\s*=\s*["\']([^"\']+)["\']',
                }
                for var, pat in patterns.items():
                    m = re.search(pat, content)
                    if m:
                        val = m.group(1)
                        if var == "user_id":    user_id    = val
                        elif var == "api_key":   api_key    = val
                        elif var == "api_secret": api_secret = val
                        elif var == "coin":      coin       = val
                if user_id and api_key and api_secret:
                    return user_id, api_key, api_secret, coin
            except Exception:
                pass

    return user_id, api_key, api_secret, coin


# ═══ Chargement credentials ══════════════════════════════════════
USER_ID, API_KEY, API_SECRET, COIN = load_credentials()

if not (USER_ID and API_KEY and API_SECRET):
    print(json.dumps({
        "error": "Credentials manquants",
        "hint": "Renseigne ANTPOOL_USER_ID/API_KEY/API_SECRET dans secrets.js, secrets.yaml ou en variables d'environnement"
    }))
    sys.exit(1)

URL     = "https://antpool.com/api/accountOverview.htm"
TIMEOUT = 15  # secondes

# ═══ Génération signature HMAC-SHA256 ════════════════════════════
nonce = str(int(time.time()))
msg   = (USER_ID + API_KEY + nonce).encode("utf-8")
sig   = hmac.new(
    API_SECRET.encode("utf-8"),
    msg,
    hashlib.sha256
).hexdigest().upper()

# ═══ Requête POST ════════════════════════════════════════════════
body = urllib.parse.urlencode({
    "key":       API_KEY,
    "nonce":     nonce,
    "signature": sig,
    "coin":      COIN,
    "userId":    USER_ID,
}).encode("utf-8")

req = urllib.request.Request(URL, data=body, method="POST")
req.add_header("Content-Type", "application/x-www-form-urlencoded")

try:
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)
        # Format Antpool : {"code": 0, "message": "ok", "data": {...}}
        if data.get("code") == 0 and data.get("data"):
            print(json.dumps(data["data"]))
            sys.exit(0)
        err_msg = data.get("message", "API error (code: %s)" % data.get("code"))
        print(json.dumps({"error": err_msg, "userId": USER_ID}))
        sys.exit(1)
except Exception as e:
    print(json.dumps({"error": str(e), "userId": USER_ID}))
    sys.exit(1)
