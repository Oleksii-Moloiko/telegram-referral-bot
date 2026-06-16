# Telegram Referral Bot

A production-ready Telegram bot built with **aiogram 3.x** and **Django 5.2** for managing referral systems with channel subscription verification.

**🚀 Deployed on Railway** | **📊 Django Admin Panel** | **⚡ Async/Await Architecture**

---

## 📋 Features

✅ **Referral System** — Generate & track personal referral links via `/start` parameter  
✅ **Channel Verification** — Users must verify Telegram channel subscription to activate referrals  
✅ **User Profiles** — Track referral statistics per user (`/profile`)  
✅ **Leaderboard** — Top users by active referrals (`/leaderboard`)  
✅ **Admin Stats** — Admin-only bot statistics and insights (`/stats`)  
✅ **Django Admin** — Full UI for managing users, referrals, and subscriptions  
✅ **Production Ready** — PostgreSQL support, environment-based config, Railway deployment  

---

## 🏗️ Architecture

```
Telegram User (polling)
        ↓
   aiogram 3.x
        ↓
    Django ORM
        ↓
SQLite (local) / PostgreSQL (production)
```

**Design Pattern:**
- **Handlers** — Command processing (start, profile, subscription, help, stats, leaderboard)
- **Services** — Business logic (user management, subscription verification, referral tracking)
- **Keyboards** — Inline & reply keyboard UIs
- **Models** — `TelegramUser` and `Referral` with optimized queries

---

## 📦 Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Bot Framework | aiogram | 3.28.2 |
| Web Framework | Django | 5.2.15 |
| Database | PostgreSQL / SQLite | - |
| Async Runtime | asyncio | built-in |
| Config Management | python-dotenv | 1.2.2 |
| Deployment | Railway | - |

---

## 📁 Project Structure

```
telegram-referral-bot/
├── bot/
│   ├── handlers/
│   │   ├── start.py          # /start command & referral link parsing
│   │   ├── profile.py        # User stats & referral count
│   │   ├── subscription.py   # Channel subscription verification
│   │   ├── help.py           # Help & command list
│   │   ├── stats.py          # Admin-only bot statistics
│   │   └── leaderboard.py    # Top referrers leaderboard
│   ├── keyboards/
│   │   └── menu.py           # Inline & reply keyboards
│   ├── services/
│   │   ├── users.py          # User CRUD operations
│   │   ├── messages.py       # Message templates
│   │   └── subscriptions.py  # Subscription verification
│   ├── env.py                # Environment variable loader
│   └── main.py               # Bot entrypoint & dispatcher setup
├── referrals/
│   ├── models.py             # TelegramUser & Referral models
│   ├── admin.py              # Django Admin configuration
│   └── migrations/           # Database migrations
├── config/
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL routing (if needed)
│   └── asgi.py / wsgi.py     # ASGI/WSGI config
├── manage.py                 # Django management CLI
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── Procfile                  # Railway deployment config
├── start.sh                  # Startup script
└── README.md                 # This file
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.9+
- Telegram Bot (get token from [@BotFather](https://t.me/botfather))
- Telegram Channel (for subscription verification)

### 1. Clone Repository

```bash
git clone https://github.com/Oleksii-Moloiko/telegram-referral-bot.git
cd telegram-referral-bot
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Telegram Bot
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
BOT_USERNAME=your_bot_username
CHANNEL_ID=-1001234567890
CHANNEL_URL=https://t.me/your_channel
ADMIN_TELEGRAM_ID=your_telegram_id

# Database (optional, SQLite used by default)
APP_ENV=local
```

### 5. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run Bot (Local)

```bash
# Terminal 1: Run Django (optional, for Admin panel at http://127.0.0.1:8000/admin/)
python manage.py runserver

# Terminal 2: Run Telegram Bot (polling)
python bot/main.py
```

---

## 🤖 Bot Commands

| Command | Description | Required |
|---------|-------------|----------|
| `/start [ref_param]` | Start bot, handle referral links | User |
| `/profile` | Show user stats & referral count | User |
| `/help` | Show available commands | User |
| `/leaderboard` | Show top 10 referrers | User |
| `/stats` | Admin-only bot statistics | Admin |

---

## 💡 Referral Flow

```
1. User starts bot with referral link: /start?start=USER_ID
   ↓
2. Bot creates TelegramUser record
   ↓
3. Bot asks user to subscribe to channel
   ↓
4. User verifies subscription (/subscribe button)
   ↓
5. If referral param exists → Create Referral record
   ↓
6. User receives personal referral link
   ↓
7. Active referrals counted only after subscription verified
```

---

## 🗄️ Data Models

### TelegramUser
```python
- telegram_id (BigIntegerField, unique, indexed)
- username (CharField)
- first_name (CharField)
- joined_channel (BooleanField)
- created_at (DateTimeField, auto)
```

### Referral
```python
- inviter (ForeignKey → TelegramUser)
- invited (OneToOneField → TelegramUser)
- active (BooleanField)
- activated_at (DateTimeField)
- created_at (DateTimeField, auto)
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| `BOT_TOKEN` | string | ✅ | Telegram bot token from BotFather |
| `BOT_USERNAME` | string | ✅ | Bot username without `@` |
| `CHANNEL_ID` | int | ✅ | Telegram channel ID (e.g., -1001234567890) |
| `CHANNEL_URL` | string | ✅ | Public channel URL (e.g., https://t.me/channel) |
| `ADMIN_TELEGRAM_ID` | int | ✅ | Your Telegram ID (for /stats command) |
| `SECRET_KEY` | string | ✅ | Django secret key (generate: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`) |
| `DEBUG` | bool | ✅ | Django debug mode (True/False) |
| `ALLOWED_HOSTS` | string | ✅ | Comma-separated hosts (e.g., localhost,127.0.0.1) |
| `DATABASE_URL` | string | ❌ | PostgreSQL URL (optional, SQLite by default) |
| `APP_ENV` | string | ❌ | Environment (local/staging/production) |

---

## 🌐 Production Deployment (Railway)

### Deploy to Railway

```bash
# 1. Push to GitHub
git push origin main

# 2. Connect GitHub repo to Railway
# https://railway.app/ → New Project → GitHub Repo

# 3. Set environment variables in Railway dashboard:
SECRET_KEY=<your-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-railway-domain>
BOT_TOKEN=<your-bot-token>
BOT_USERNAME=<your-bot-username>
CHANNEL_ID=<channel-id>
CHANNEL_URL=<channel-url>
ADMIN_TELEGRAM_ID=<your-id>
DATABASE_URL=postgresql://...  # Railway provides this

# 4. Railway auto-deploys on git push
```

**Procfile:**
```
worker: ./start.sh
```

The bot runs as a **worker process** (not web service) using **polling** to check for Telegram updates.

---

## 📊 Admin Panel

Access Django Admin at: `http://your-domain/admin/`

**Manage:**
- 👥 **TelegramUser** — View/edit users, subscription status
- 🔗 **Referral** — View/activate referrals, see chains
- 📈 **Filters** — Filter by active status, date joined, etc.

---

## 🐛 Development & Debugging

### Run Tests
```bash
python manage.py test
```

### Django Shell
```bash
python manage.py shell
```

```python
from referrals.models import TelegramUser, Referral

# Get user
user = TelegramUser.objects.get(telegram_id=123456789)

# Count active referrals
user.referrals.filter(active=True).count()

# Find who referred this user
user.invited_by.inviter.username
```

### Check Bot Logs

```bash
# Railway logs
railway logs

# Local logs (stdout)
python bot/main.py
```

---

## 📝 Known Limitations

- **Polling Model** — Updates checked every ~30-45 seconds (not real-time webhooks)
- **Single Referrer** — Each user can only have one inviter (`OneToOneField` constraint)
- **No Rate Limiting** — Bot processes all requests without throttling
- **Manual Admin** — Currently no self-service referral management UI
- **No Notifications** — No email/SMS notifications to referrers

---

## 🎯 Future Enhancements

- [ ] Webhook support instead of polling (faster updates)
- [ ] Rate limiting & spam protection
- [ ] Email/SMS notifications for new referrals
- [ ] Web dashboard for users (referral stats, links)
- [ ] Unit tests + CI/CD pipeline
- [ ] Multi-language support
- [ ] Referral rewards system

---

## 📄 License

This project is open source under the MIT License.

---

## 🤝 Contributing

This is a pet project. Feel free to fork and modify for your use case!

---

## 📧 Support

For issues or questions:
1. Check Django logs: `python manage.py check`
2. Check bot logs: Run `python bot/main.py` locally
3. Verify environment variables are set correctly

---

**Last Updated:** June 2026  
**Status:** ✅ Production Ready  
**Deployment:** Railway (worker process)  
**Python Version:** 3.9+  
**Django Version:** 5.2.15  
**aiogram Version:** 3.28.2
