# ==============================
# TELEGRAM MUSIC BOT - CONFIG
# ==============================
# Ye saari values fill karo apne credentials ke saath

# my.telegram.org se milega (App banane par)
API_ID = "12345678"          # <-- apna API_ID daalo (number)
API_HASH = "your_api_hash_here"   # <-- apna API_HASH daalo

# BotFather se banaye gaye bot ka token
BOT_TOKEN = "your_bot_token_here"

# Assistant/Userbot account ki session string
# (Ye account voice chat join karega, kyunki normal bots VC join nahi kar sakte)
# Session string generate karne ke liye neeci "generate_session.py" file chalao
SESSION_STRING = "your_session_string_here"

# Bot ka naam (logs/prefix ke liye)
BOT_NAME = "MyMusicBot"

# Spotify Developer Dashboard (https://developer.spotify.com/dashboard) se milega
# Ye sirf METADATA (gaane ka naam, artist, album) fetch karne ke liye use hota hai —
# actual audio YouTube se hi aata hai (Spotify seedha audio download allow nahi karta)
SPOTIFY_CLIENT_ID = "your_spotify_client_id_here"
SPOTIFY_CLIENT_SECRET = "your_spotify_client_secret_here"

# ==============================
# FORCE-SUBSCRIBE (AUTH CHANNEL / AUTH GROUP)
# ==============================
# Jab tak user in dono ko join nahi karega, bot ke commands kaam nahi karenge.
# Username daalo BINA @ ke (jaise "mychannel"), ya khaali "" rakho agar
# ye feature disable karna hai.
#
# ⚠️ Bot account (aur agar possible ho to assistant account bhi) ko is
# channel/group ka MEMBER (ya admin) hona zaroori hai, tabhi wo membership
# check kar payega.
AUTH_CHANNEL = ""   # e.g. "mychannel"  (bina @ ke)
AUTH_GROUP = ""     # e.g. "mygroup"    (bina @ ke)

# ==============================
# MONGODB DATABASE
# ==============================
# Free MongoDB Atlas cluster banao: https://www.mongodb.com/cloud/atlas/register
# Connection string "Connect" button se milegi (Drivers option choose karo)
MONGO_URI = "mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "music_bot_db"

# ==============================
# LOG CHANNEL
# ==============================
# Jab bhi koi naya group bot ko activate karega, ya koi important
# error aayega, uska log is channel me bhej diya jayega.
# Channel ka username daalo BINA @ ke, ya uski numeric ID (jaise -1001234567890).
# Khaali "" rakhne par logging disable ho jayegi.
#
# ⚠️ Bot account ko is channel ka MEMBER/ADMIN hona zaroori hai taaki wo
# wahan message bhej sake.
LOG_CHANNEL = ""   # e.g. "mylogschannel" ya -1001234567890

# ==============================
# START MENU LINKS (Optional)
# ==============================
# /start menu me "Join Channel" aur "Join Group" buttons dikhane ke liye.
# Ye sirf PROMOTIONAL links hain (Auth Channel/Group jaisa mandatory nahi hai) —
# khaali "" rakhne par wo button hi nahi dikhega.
UPDATES_CHANNEL = ""   # e.g. "mychannel"  (bina @ ke)
SUPPORT_GROUP = ""     # e.g. "mygroup"    (bina @ ke)
