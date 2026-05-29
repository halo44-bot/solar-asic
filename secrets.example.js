// ═══════════════════════════════════════════════════════════════
// SECRETS.JS — Configuration Solar ASIC Dashboard
// ⚠️  NE JAMAIS COMMITER CE FICHIER SUR GITHUB
// Copiez ce fichier : cp secrets.example.js secrets.js
// Puis remplissez vos vraies valeurs.
// Emplacement : /config/www/secrets.js
// ═══════════════════════════════════════════════════════════════

// ── Home Assistant ────────────────────────────────────────────
const HA_URL_LOCAL = 'http://192.168.1.XX:8123';      // IP locale de votre HA
const HA_URL_VPN   = 'http://100.XX.XX.XX:8123';      // IP Tailscale / VPN (optionnel)
const HA_TOKEN     = 'REMPLACER_PAR_TOKEN_HA_LONGUE_DUREE';
// Obtenir dans HA → Profil → Sécurité → Jetons longue durée

// ── F2Pool ────────────────────────────────────────────────────
const F2POOL_USER  = 'votre_username_f2pool';
const F2POOL_TOKEN = 'votre_token_api_f2pool';
// Obtenir sur https://www.f2pool.com → Settings → API

// ── Antpool (optionnel, si vous minez du KDA) ─────────────────
const ANTPOOL_USER_ID = '';   // ex: 'SZXXXXXXXXXX'
const ANTPOOL_API_KEY = '';   // ex: 'your_api_key_here'
const ANTPOOL_SECRET  = '';   // ex: 'your_secret_here'
// Obtenir sur https://www.antpool.com → Settings → API

// ── K1Pool (optionnel, si vous minez du RXD) ──────────────────
const K1POOL_RXD_WALLET = ''; // ex: 'your_rxd_wallet_address'

// ── Telegram (optionnel, pour les notifications) ──────────────
const TELEGRAM_BOT_TOKEN = ''; // ex: '123456:AABBcc...'
const TELEGRAM_CHAT_ID   = ''; // ex: '987654321'
// Créer un bot via @BotFather sur Telegram

// ── HA Companion (optionnel) ──────────────────────────────────
const HA_NOTIFY_SERVICE = ''; // ex: 'notify.mobile_app_mon_telephone'

// ── Bannière (optionnel) ──────────────────────────────────────
const BANNER_JSON_URL = '';
// URL d'un fichier JSON distant pour afficher des annonces sur le dashboard
// Ex: 'https://raw.githubusercontent.com/user/repo/main/banner.json'

// ═══════════════════════════════════════════════════════════════
// MINING_COINS — Liste des cryptomonnaies minées
// ═══════════════════════════════════════════════════════════════
// Adaptez cette liste à VOS cryptos.
// pool: 'f2pool' (défaut) | 'k1pool' | 'antpool'
//
// ⚠️ OBLIGATOIRE — sans cette variable le dashboard ne charge pas les revenus
// ═══════════════════════════════════════════════════════════════
const MINING_COINS = [
  { id:'bitcoin',  symbol:'BTC',  name:'Bitcoin',  coingecko:'bitcoin',  decimals:8, color:'#f59e0b' },
  { id:'alephium', symbol:'ALPH', name:'Alephium', coingecko:'alephium', decimals:4, color:'#10b981' },
  { id:'kaspa',    symbol:'KAS',  name:'Kaspa',    coingecko:'kaspa',    decimals:4, color:'#70c7ba' },
  // Exemples de cryptos sur d'autres pools :
  // { id:'radiant',  symbol:'RXD',  name:'Radiant',  coingecko:'radiant',  decimals:4, color:'#8b5cf6', pool:'k1pool' },
  // { id:'kadena',   symbol:'KDA',  name:'Kadena',   coingecko:'kadena',   decimals:4, color:'#ed098f', pool:'antpool' },
  // { id:'litecoin', symbol:'LTC',  name:'Litecoin', coingecko:'litecoin', decimals:5, color:'#bfbfbf' },
];
