# 🎶 Telegram Music Bot — Complete Setup Guide

Ek full-featured Telegram Music Bot jo group chats me voice chat streaming, MP3/MP4
download, Spotify integration, aur bahut kuch support karta hai — MongoDB database,
multi-language, aur admin-security ke saath.

---

## 📋 Table of Contents

1. [Features Overview](#-features-overview)
2. [Project Structure](#-project-structure)
3. [Activation Rules (Important)](#️-zaroori-activation-rules)
4. [Setup Steps](#-setup-steps)
5. [Commands List](#-commands-list)
6. [Deployment on Render.com](#-24x7-chalane-ke-liye-deployment-on-rendercom)
7. [Troubleshooting](#-troubleshooting)
8. [FAQ](#-faq)
9. [Important Notes](#-important-notes)

---

## 🚀 Features Overview

| Feature | Description |
|---|---|
| 🎵 Voice Chat Streaming | `/play` se live gaana group ki voice chat me bajta hai |
| 📃 Playlist Support | YouTube playlist link doge to poori playlist queue ho jayegi |
| ⏯️ Full Playback Control | Pause, resume, skip, stop, queue, shuffle, loop |
| 🔊 Volume Control | 0-200% tak volume adjust kar sakte ho |
| 🖲️ Inline Buttons | Player message ke neeche hi control buttons |
| 📥 YouTube MP3 | `/song` se direct MP3 file group me milti hai |
| 🟢 Spotify Support | `/spotify` se Spotify link/naam se MP3 milta hai |
| 🎬 Video Download | `/video` se MP4 file, `/vlink` se direct streaming link |
| 📜 Lyrics | `/lyrics` se kisi bhi gaane ke lyrics |
| 🌐 Multi-language | Hindi aur English dono me bot use kar sakte ho (per-group) |
| 🔒 Admin-Only Operation | Bot sirf tabhi kaam karega jab use group me Admin banaya ho |
| ✅ One-time Activation | `/start` sirf ek baar chalega, phir hamesha activate rahega |
| 📢 Force-Subscribe | Auth Channel/Group join karna zaroori kar sakte ho |
| 🗄️ MongoDB Database | Saara data persistently save hota hai (restart-proof) |
| 📋 Log Channel | Naye group activations ka record ek channel me milta hai |

---

## 📁 Project Structure

```
music_bot/
├── main.py                  # Bot ka entry point — sab kuch yahin se start hota hai
├── config.py                 # SAARI credentials aur settings yahan daalni hain
├── generate_session.py       # Assistant account ki session string banane ke liye
├── db.py                     # MongoDB connection aur data functions
├── guard.py                  # Admin-check + one-time activation logic
├── fsub.py                   # Auth Channel/Group (force-subscribe) logic
├── logger.py                 # Log Channel me events bhejne ka logic
├── language.py               # Hindi/English translations + language switching
├── requirements.txt          # Saari Python libraries ki list
├── README.md                  # Ye file
└── plugins/                  # Har command yahan alag file me hai
    ├── start.py               # /start, /help
    ├── play.py                 # /play, /pause, /resume, /skip, /stop, /queue, /shuffle, /loop, /volume
    ├── song.py                  # /song (YouTube MP3)
    ├── spotify.py                # /spotify (Spotify MP3)
    ├── video.py                   # /video, /vlink
    ├── lyrics.py                   # /lyrics
    └── language_cmd.py             # /language
```

`main.py` startup par `plugins/` folder ki saari files **automatically** load kar leta
hai — koi naya command add karna ho to bas `plugins/` me nayi file daal do, register()
function likh do, aur wo apne aap load ho jayegi.

---

## ⚠️ Zaroori: Activation Rules

Bot kaam kaise karta hai, ye 4 rules zaroor samajh lo:

1. **Bot Admin hona zaroori hai** — Kisi bhi group me bot tabhi kaam karega jab use
   **Admin** banaya gaya ho. Iske bina koi bhi command chalegi hi nahi.
2. **`/start` sirf ek baar** — Group me pehli baar `/start` bhejne se wo group
   **permanently activate** ho jata hai (MongoDB me save hota hai). Dubara `/start`
   karne ki zaroorat nahi hai, bot restart ho ya server change ho, activation yaad
   rehta hai.
3. **Admin check `/start` par bhi hota hai** — Agar bot admin nahi hai to `/start`
   khud fail ho jayega aur bata dega "pehle admin banao".
4. **Auth Channel/Group (agar set hai)** — Agar tumne Force-Subscribe set kiya hai,
   to har user ko wo channel/group join karna hoga, tabhi uske liye koi bhi command
   kaam karegi (chahe group activate ho ya na ho).

---

## 🛠 Setup Steps

### Step 0 (Optional): Auth Channel / Auth Group set karo

Agar chahte ho ki bot sirf unhi logo ke liye kaam kare jo tumhara channel/group join
kiye hue hain (Force-Subscribe), to `config.py` me:

```python
AUTH_CHANNEL = "mychannel"   # bina @ ke apne channel ka username
AUTH_GROUP = "mygroup"       # bina @ ke apne group ka username
```

⚠️ **Important:** Bot account ko khud us channel/group ka member (ya admin) hona
zaroori hai, tabhi wo doosre users ki membership check kar payega. Agar ye feature
nahi chahiye to dono ko khaali `""` rehne do (default).

### Step 0.5: MongoDB Database setup karo (zaroori hai)

Bot saara persistent data (activated groups, language settings) **MongoDB** me store
karta hai — taaki bot restart ho ya kahin bhi deploy karo, data safe rahe.

1. https://www.mongodb.com/cloud/atlas/register par jao aur **free account** banao
2. Ek **free cluster** create karo (M0 tier — hamesha free hai)
3. **Database Access** me ek user banao (username/password set karo — password yaad
   rakh lena)
4. **Network Access** me `0.0.0.0/0` add karo (sab IPs se access — simple setup ke
   liye; production me chaho to apne server ki IP tak limit kar sakte ho)
5. Cluster par **"Connect"** → **"Drivers"** → connection string copy karo, kuch aisa
   dikhega:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
6. Ye string `config.py` ke `MONGO_URI` me daal do (apna asli username/password bhi
   usme daal do — `<password>` jagah par apna password likhna mat bhoolna)

```python
MONGO_URI = "mongodb+srv://tumhara_username:tumhara_password@cluster.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "music_bot_db"
```

Bot start hote hi terminal me confirm ho jayega ki MongoDB connect ho gaya hai
("MongoDB connected — X activated groups aur Y language settings load ho gayi").

### Step 0.6 (Optional): Log Channel set karo

Jab bhi koi naya group bot ko `/start` se activate karega, uska record (group naam,
ID, members count, kisne activate kiya) ek channel me automatically log ho sakta hai.

1. Ek Telegram channel banao (private ya public, dono chalega)
2. Bot account ko us channel me add karke **member/admin** bana do
3. Channel ka username (bina `@`) ya numeric ID `config.py` me daal do:

```python
LOG_CHANNEL = "mylogschannel"   # ya -1001234567890 (channel ki numeric ID)
```

Agar ye feature nahi chahiye to `LOG_CHANNEL = ""` hi rehne do (default disabled hai).

### Step 0.7 (Optional): `/start` menu me Join Channel/Group buttons

`/start` command me "Join Channel" aur "Join Group" buttons dikhane ke liye (promotional
links — Auth Channel/Group jaisa mandatory nahi hai):

```python
UPDATES_CHANNEL = "mychannel"   # apna updates channel (bina @ ke)
SUPPORT_GROUP = "mygroup"       # apna support group (bina @ ke)
```

Khaali `""` rakhne par wo button bas dikhega hi nahi.

📌 Yehi `UPDATES_CHANNEL` `/song`, `/video`, `/spotify` se milne wali files ke saath
bhi "Join Updates Channel" button aur "Powered By" wala stylish caption laga deta hai.

### Step 1: Zaroori cheezein install karo

Python 3.9+ aur FFmpeg system me install hona chahiye.

```bash
# FFmpeg install karo (Linux/Ubuntu)
sudo apt update && sudo apt install ffmpeg -y

# Mac (Homebrew se)
brew install ffmpeg

# Windows: https://ffmpeg.org/download.html se download karke PATH me add karo

# Python libraries install karo
pip install -r requirements.txt
```

### Step 2: Telegram API credentials lo

1. https://my.telegram.org par jao aur login karo (apne normal number se)
2. "API Development Tools" me jao
3. Ek app banao — **API_ID** aur **API_HASH** milega
4. Ye dono `config.py` me daal do

### Step 2.5: Spotify API credentials lo (Spotify se download karne ke liye)

1. https://developer.spotify.com/dashboard par jao aur login karo (free account
   chalega)
2. **"Create App"** par click karo — naam kuch bhi daal do, Redirect URI me
   `http://localhost` daal do
3. App ke andar **Client ID** aur **Client Secret** milega
4. Dono `config.py` ke `SPOTIFY_CLIENT_ID` aur `SPOTIFY_CLIENT_SECRET` me daal do

> **Note:** Spotify apna audio seedha download nahi karne deta. `spotdl` tool
> Spotify se sirf gaane ka naam/artist/album (metadata) leta hai, aur phir wahi
> gaana YouTube par dhoond kar uska audio download karta hai.

### Step 3: Bot banao (BotFather se)

1. Telegram me `@BotFather` ko message karo
2. `/newbot` bhejo aur naam/username set karo
3. Jo **token** milega, use `config.py` ke `BOT_TOKEN` me daal do
4. BotFather ko `/setprivacy` bhejo, apna bot select karo, aur **Disable** kar do
   (taaki bot group ke saare messages padh sake, sirf commands nahi)

### Step 4: Assistant account ki session string banao

Voice chat me join karne ke liye ek normal Telegram account (assistant) chahiye —
kyunki bots khud voice/video chat join nahi kar sakte.

```bash
python generate_session.py
```

- Apna API_ID aur API_HASH daalo
- Phone number daalo (assistant account ka — apna doosra number bhi chal sakta hai)
- OTP daalo
- Jo session string milegi, use `config.py` ke `SESSION_STRING` me paste kar do

⚠️ **Ye session string kisi ke saath share mat karna** — isse poora account access
mil jata hai, exactly password jaisa sensitive hai.

### Step 5: Dono accounts ko group me add karo

- **Bot** ko group me add karo aur use **Admin** banao (Voice chats manage karne ki
  permission ke saath) — ye zaroori hai, iske bina koi command kaam nahi karega
- **Assistant account** ko bhi usi group me add karo (ye voice chat join karega)

### Step 6: Group me ek baar `/start` bhejo

Group me `/start` command bhejo. Ye check karega ki bot admin hai ya nahi:

- Agar admin hai → group **permanently activate** ho jayega, ab sab commands kaam
  karenge, aur (agar set hai) Log Channel me ek entry bhi ban jayegi
- Agar admin nahi hai → bot bata dega ki pehle admin banao

⚠️ Ye sirf **ek baar** karna hai — dubara activate karne ki zaroorat nahi, chahe bot
restart ho jaye ya naye server par deploy karo (MongoDB me record rehta hai).

### Step 7: Bot chalao

```bash
python main.py
```

Agar sab sahi hai to terminal me kuch aisa dikhega:

```
MongoDB se connect ho raha hai...
MongoDB connected — 0 activated groups aur 0 language settings load ho gayi.
MyMusicBot start ho gaya hai! Bot aur assistant dono online hain.
Bot ko group me add karo, aur assistant account ko bhi group me add karo.
```

---

## 📜 Commands List

Sab commands **group chat me** kaam karte hain (activation aur admin requirement ke
saath), aur **sab group members** use kar sakte hain.

| Command | Kaam |
|---|---|
| `/start` | Bot ko activate/confirm karta hai (group me bhi, private me bhi) |
| `/help` | Sabhi commands + usage rules ki list dikhata hai |
| `/about` | Bot ke baare me jaankari dikhata hai |
| `/play <naam/link>` | Voice chat me live gaana stream karta hai (playlist link bhi chalega) |
| `/pause` | Music pause karta hai |
| `/resume` | Music resume karta hai |
| `/skip` | Agla gaana queue se bajata hai |
| `/stop` | Music band karke voice chat se nikal jata hai |
| `/queue` | Current gaana + aage ki queue dikhata hai |
| `/shuffle` | Queue ko random order me mix karta hai |
| `/loop [off/song/queue]` | Loop mode set karta hai (bina argument diye cycle karta hai) |
| `/volume <0-200>` | Voice chat ka volume set karta hai |
| `/lyrics <naam>` | Gaane ke lyrics dhoond kar bhejta hai |
| `/song <naam>` | Seedha MP3 file bhejta hai (YouTube se, voice chat ke bina) |
| `/spotify <link/naam>` | Spotify link ya gaane ka naam deke MP3 file bhejta hai |
| `/language hindi` / `/language english` | Group ki language switch karta hai |
| `/video <naam/link>` | Video ko MP4 file ke roop me download karke group me bhejta hai |
| `/vlink <naam/link>` | Bina download kiye, seedha temporary streaming/download link deta hai |

Player message ke neeche ⏸/▶️, ⏭, ⏹, 🔀, 🔁 wale **inline buttons** bhi hote hain —
directly button dabakar bhi control kiya ja sakta hai, command likhne ki zaroorat
nahi.

---

## 🌐 24x7 Chalane Ke Liye (Deployment on Render.com)

Local computer band hone par bot bhi band ho jayega. Hamesha online rakhne ke liye
**Render.com** use karo (free tier available hai):

### Render par deploy karne ke steps:

1. Apna code GitHub repo me push karo (public ya private, dono chalega)
2. https://render.com par jao aur account banao (GitHub se sign up kar sakte ho)
3. Dashboard me **"New +"** → **"Background Worker"** choose karo
   (⚠️ "Web Service" mat choose karna — ye bot koi HTTP server nahi chalata,
   isliye **Background Worker** hi sahi option hai)
4. Apna GitHub repo connect karo
5. Settings me:
   - **Runtime:** Python 3
   - **Build Command:**
     ```bash
     apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     python main.py
     ```
6. `config.py` ki jagah **Environment Variables** use karna better hai (taaki
   credentials GitHub par public na dikhein) — Render dashboard me **"Environment"**
   tab me sab keys add karo (`API_ID`, `API_HASH`, `BOT_TOKEN`, `SESSION_STRING`,
   `MONGO_URI`, etc.) aur `config.py` ko unhe `os.environ.get(...)` se read karne
   ke liye update kar do
7. **"Create Background Worker"** par click karo — Render apne aap build karke bot
   start kar dega

### Render Free Tier ka ek zaroori note:

Render ka free tier **Background Worker** ko kabhi-kabhi inactivity ke baad restart
kar sakta hai. Chunki is bot ka saara persistent data (activation, language) ab
**MongoDB** me hai, restart hone par bhi kuch data loss nahi hoga — bot turant
wapas kaam karne lagega.

Logs dekhne ke liye Render dashboard ke **"Logs"** tab me jao — wahi terminal output
dikhega jo local machine par `python main.py` chalane par dikhta.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---|---|
| `/start` bolta hai "pehle admin banao" | Group settings me jaake bot ko Admin banao, phir `/start` dubara bhejo |
| Koi command response hi nahi de raha | Check karo bot khud ON hai (`python main.py` chal raha hai terminal me) |
| `/play` "voice chat join nahi ho paya" bolta hai | Group me voice chat pehle se **start/active** honi chahiye — bot khud voice chat start nahi karta |
| MongoDB connection error aa raha hai | `MONGO_URI` sahi se copy hua ya nahi check karo, aur Network Access me `0.0.0.0/0` add kiya ya nahi |
| Spotify download fail ho raha hai | `SPOTIFY_CLIENT_ID`/`SECRET` sahi hain check karo, aur `spotdl` install hai ya nahi (`pip install spotdl`) |
| Video bahut bada hai, bhej nahi pa raha | 50MB se bada video default Bot API se nahi jaayega — `/vlink` use karo ya Local Bot API Server setup karo |
| Session string generate karte time error | Sahi API_ID/API_HASH use karo, aur normal user account (bot account nahi) ka phone number daalo |
| Auth Channel wala message baar-baar aa raha hai | User ne channel/group abhi tak join nahi kiya — join karne ke baad turant kaam karega |
| Bot group me kuch reply hi nahi karta | BotFather me `/setprivacy` → **Disable** kiya ya nahi check karo |

---

## ❓ FAQ

**Q: Kya ye bot free hai chalane ke liye?**
Haan — saari services (Telegram API, MongoDB Atlas free tier, Spotify Developer API,
YouTube via yt-dlp, Render.com free tier) free hain.

**Q: Assistant account kyun chahiye?**
Telegram bots khud voice/video chat join nahi kar sakte — sirf normal user accounts
kar sakte hain. Isliye ek "assistant" account chahiye jo voice chat join kare, aur
bot use commands ke through control kare.

**Q: Kya ek hi assistant account multiple groups me use ho sakta hai?**
Haan, ek assistant account ek saath multiple groups ki voice chats handle kar sakta
hai (jab tak Telegram ki apni per-account limits allow karein).

**Q: Kya main is bot ko multiple bots ke liye use kar sakta hoon?**
Haan, bas alag `BOT_TOKEN` aur (agar chaho to) alag assistant account use karo. Baaki
sab code same rahega.

**Q: MongoDB free tier me kitna data store ho sakta hai?**
M0 free tier me 512MB tak — is bot ke liye (sirf group IDs aur language settings
store hoti hain) ye hazaro groups ke liye kaafi hai.

**Q: `/song` aur `/spotify` me kya fark hai?**
`/song` YouTube se seedha search karta hai. `/spotify` Spotify se gaane ka sahi
naam/artist metadata leta hai (jyada accurate match) aur phir YouTube se hi audio
download karta hai.

---

## ⚠️ Important Notes

- YouTube se content stream/download karna unke Terms of Service ke against ho sakta
  hai — personal/educational use tak hi limit rakhna behtar hai.
- Bade groups me bahut zyada `/song` ya `/spotify` use karne se rate-limit ya ban ho
  sakta hai — thoda savdhaani se use karo.
- Agar `/play` error de raha hai, check karo ki group me voice chat **already
  active/started** hai — bot khud voice chat start nahi karta, usme sirf join karta
  hai.
- `/video` command 720p tak ki video download karta hai taaki file size manageable
  rahe. Default Telegram Bot API (cloud) par file upload limit **50MB** hoti hai —
  bade video bhejne ke liye apna **Local Bot API Server** run karna padega (jisse
  limit 2GB tak ho jaati hai). Agar wo setup nahi karna, to `/vlink` use karo — wo
  bina download kiye seedha temporary streaming link de deta hai.
- `/vlink` se milne wala link YouTube ki taraf se generate hota hai aur kuch ghanto
  me expire ho sakta hai.
- **`/start`** private chat me bot ki welcome screen dikhata hai (Add to Group button
  ke saath), aur **group me** bot ko admin-check karke permanently activate karta
  hai.
- Group ki activation aur language settings **MongoDB** me save hoti hain — data
  hamesha safe rehta hai, bot restart ya server change hone par bhi.
- Agar bot ko group me admin se hata diya jaye, to commands "bot admin nahi hai"
  bolke ruk jayenge — dubara admin banao to wapas kaam karne lagenge (dubara
  `/start` ki zaroorat nahi).
- `config.py` me daali gayi saari keys/tokens (BOT_TOKEN, SESSION_STRING, MONGO_URI,
  Spotify credentials) **sensitive** hain — kabhi bhi public repo ya kisi aur ke
  saath share mat karna.
