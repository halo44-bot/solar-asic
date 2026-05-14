// ═══════════════════════════════════════════════════════════════
// secrets.example.js — Template de configuration
//
// 1. Copie ce fichier en `secrets.js` dans /config/www/ de Home Assistant
//    (cp secrets.example.js secrets.js)
// 2. Remplis TES propres valeurs
// 3. NE JAMAIS commiter secrets.js (déjà dans .gitignore)
// ═══════════════════════════════════════════════════════════════

// ── Home Assistant ────────────────────────────────────────────
const HA_URL_LOCAL = 'http://192.168.1.X:8123';       // TODO: ton IP locale HA
const HA_URL_VPN   = 'https://ton-ha.duckdns.org';    // TODO: URL externe (ou même valeur)
const HA_TOKEN     = 'COLLE_TON_TOKEN_HA_ICI';        // Profil HA → Tokens longue durée

// ── Pools de minage ───────────────────────────────────────────
// Nom d'utilisateur F2Pool (laisser '' si non utilisé)
const F2POOL_USER = '';

// Cryptos minées — décommenter celles que tu mines
const MINING_COINS = [
  // { id: 'alph',    symbol: 'ALPH', color: '#fa792b', decimals: 3, coingecko: 'alephium' },
  // { id: 'bitcoin', symbol: 'BTC',  color: '#f7931a', decimals: 8, coingecko: 'bitcoin'  },
  // { id: 'kda',     symbol: 'KDA',  color: '#e41d63', decimals: 4, coingecko: 'kadena'   },
  // { id: 'rxd',     symbol: 'RXD',  color: '#ff5c57', decimals: 4, coingecko: 'radiant'  },
  // { id: 'kas',     symbol: 'KAS',  color: '#49dbc0', decimals: 3, coingecko: 'kaspa'    },
  // { id: 'ltc',     symbol: 'LTC',  color: '#345d9d', decimals: 6, coingecko: 'litecoin' },
];

// ── Antpool API (pour KDA uniquement) ─────────────────────────
// Récupère ces clés sur https://antpool.com/userCenter/apiAccess.htm
const ANTPOOL_USER_ID    = '';   // ex: "SZCC88XXXXXXXXXX"
const ANTPOOL_API_KEY    = '';   // 32 caractères hex
const ANTPOOL_API_SECRET = '';   // 32 caractères hex
const ANTPOOL_COIN       = 'KDA';

// ── Notifications (laisser '' pour désactiver) ────────────────
const TELEGRAM_BOT_TOKEN = '';   // @BotFather pour créer un bot
const TELEGRAM_CHAT_ID   = '';   // ID de ton chat Telegram
const NTFY_TOPIC         = '';   // ex: 'mon-topic-unique-solar-asic'
const NTFY_SERVER        = 'https://ntfy.sh';
const HA_NOTIFY_SERVICE  = '';   // ex: 'notify.mobile_app_mon_telephone'

// ── Bannière distante (optionnel) ─────────────────────────────
// URL vers un banner.json sur ton propre GitHub/serveur
// Laisser '' pour désactiver
const BANNER_JSON_URL = '';
