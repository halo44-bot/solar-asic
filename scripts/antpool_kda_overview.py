#!/usr/bin/env python3
"""
Antpool KDA Overview — Récupère hashrate + workers depuis accountOverview.htm
Lancé toutes les 5 min par HA command_line sensor.
Affiche TOUTES les erreurs/réponses pour debug.
"""
import hmac
import hashlib
import time
import json
import sys
import urllib.request
import urllib.parse
import urllib.error

USER_ID    = "TON_USER_ID"
API_KEY    = "TA_CLE_API_32_CHARS_HEX"
API_SECRET = "TON_API_SECRET_32_CHARS_HEX"
COIN       = "KDA"
URL        = "https://antpool.com/api/accountOverview.htm"

def try_request(nonce_value):
    """Essaie un appel API avec le nonce donné."""
    msg = (USER_ID + API_KEY + nonce_value).encode("utf-8")
    sig = hmac.new(API_SECRET.encode("utf-8"), msg, hashlib.sha256).hexdigest().upper()
    body = urllib.parse.urlencode({
        "userId":    USER_ID,
        "key":       API_KEY,
        "coin":      COIN,
        "nonce":     nonce_value,
        "signature": sig,
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            return raw, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"URL error: {e.reason}"
    except Exception as e:
        return None, f"Exception: {type(e).__name__}: {e}"

# Tente d'abord nonce en SECONDES (comme PowerShell qui marche)
nonce_s = str(int(time.time()))
raw, err = try_request(nonce_s)
attempt = "secondes"

# Si échec ou data vide, retente en MILLISECONDES
if raw is None or '"data":null' in (raw or "") or '"code":-1' in (raw or ""):
    nonce_ms = str(int(time.time() * 1000))
    raw, err = try_request(nonce_ms)
    attempt = "millisecondes"

if raw is None:
    # Échec total — retourne un JSON d'erreur
    print(json.dumps({
        "data": {"hsLast10m": 0, "hsLast1d": 0, "activeWorkerNum": 0, "totalWorkerNum": 0},
        "_error": err or "unknown",
        "_attempt": attempt
    }))
    sys.exit(1)

# Parse la réponse Antpool
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(json.dumps({
        "data": {"hsLast10m": 0, "hsLast1d": 0, "activeWorkerNum": 0, "totalWorkerNum": 0},
        "_error": f"JSON decode: {e}",
        "_raw": raw[:200]
    }))
    sys.exit(1)

# Antpool format : {"code": 0, "message": "ok", "data": {...}}
if data.get("code") == 0 and data.get("data"):
    # SUCCES — on sort le JSON complet (compatible avec value_template existant)
    print(json.dumps(data))
    sys.exit(0)

# API a répondu mais avec erreur
print(json.dumps({
    "data": {"hsLast10m": 0, "hsLast1d": 0, "activeWorkerNum": 0, "totalWorkerNum": 0},
    "_error": data.get("message", "API code " + str(data.get("code", "?"))),
    "_full_response": data
}))
sys.exit(1)
