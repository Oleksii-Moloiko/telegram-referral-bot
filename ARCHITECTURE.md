# Architecture & Design Decisions

## Overview

This document outlines the architectural decisions and design patterns used in the Telegram Referral Bot.

---

## System Design

### High-Level Flow

```
┌─────────────────┐
│  Telegram User  │
└────────┬────────┘
         │ (sends /start, /profile, etc.)
         ↓
┌─────────────────────────┐
│   aiogram Dispatcher    │  ← Polling every ~30-45s
├─────────────────────────┤
│  Router (commands)      │
│  - start_router         │
│  - profile_router       │
│  - subscription_router  │
│  - help_router          │
│  - stats_router         │
│  - leaderboard_router   │
└────────┬────────────────┘
         │ (processes commands)
         ↓
┌──────────────────────────┐
│   Handler Functions      │
│  (bot/handlers/*.py)     │
└────────┬─────────────────┘
         │ (calls services)
         ↓
┌──────────────────────────┐
│  Business Logic Services │
│  (bot/services/*.py)     │
│  - user management       │
│  - subscription verify   │
│  - message templates     │
└────────┬─────────────────┘
         │ (ORM queries)
         ↓
┌──────────────────────────┐
│    Django ORM Models     │
│   (referrals/models.py)  │
│  - TelegramUser          │
│  - Referral              │
└────────┬─────────────────┘
         │ (SQL queries)
         ↓
┌──────────────────────────┐
│   PostgreSQL / SQLite    │
└──────────────────────────┘
```

---

## Directory Structure & Responsibilities

### `/bot` — Telegram Bot Logic

```
bot/
├── main.py              # Bot initialization, dispatcher setup, polling loop
├── env.py               # Environment variable loading
├── handlers/            # Command handlers (async functions)
│   ├── start.py         # /start command + referral link parsing
│   ├── profile.py       # /profile user stats
│   ├── subscription.py  # /subscribe verification
│   ├── help.py          # /help command list
│   ├── stats.py         # /stats admin-only
│   └── leaderboard.py   # /leaderboard top referrers
├── services/            # Business logic layer
│   ├── users.py         # User CRUD (get_or_create, update_user)
│   ├── subscriptions.py # Check channel membership
│   └── messages.py      # Message text templates
└── keyboards/           # UI components
    └── menu.py          # Inline & reply keyboard buttons
```

**Design Pattern:** Handler → Service → ORM

Each handler is a simple async function that:
1. Extracts data from Telegram update
2. Calls service functions for business logic
3. Sends response message via bot.send_message()

---

### `/referrals` — Django App

```
referrals/
├── models.py            # Data models (TelegramUser, Referral)
├── admin.py             # Django Admin configuration
├── apps.py              # App config
├── tests.py             # Unit tests (optional)
├── views.py             # API views (not used in bot version)
└── migrations/          # Database migrations
    ├── 0001_initial.py
    ├── 0002_...
    ├── 0003_...
    └── 0004_...
```

**Models:**
- `TelegramUser` — Stores bot user info (telegram_id, username, subscription status)
- `Referral` — Links inviter → invited user, tracks activation

---

### `/config` — Django Settings

```
config/
├── settings.py          # Django config (database, installed apps, etc.)
├── urls.py              # URL routing (Django Admin)
├── wsgi.py              # Production WSGI server config
└── asgi.py              # ASGI config (optional)
```

---

## Key Design Decisions

### 1. **Async/Await Architecture (aiogram 3.x)**

**Why?**
- Telegram polling requires concurrent request handling
- Multiple users can send commands simultaneously
- Non-blocking I/O improves throughput

**Implementation:**
- All handlers are `async def`
- Database queries wrapped with `sync_to_async()` where needed
- Bot polling runs in single event loop

```python
async def start_handler(message: Message):
    user = await sync_to_async(TelegramUser.objects.get_or_create)(telegram_id=message.from_user.id)
    await message.answer("Welcome!")
```

---

### 2. **Service Layer Abstraction**

**Why?**
- Separates Telegram logic from business logic
- Easier to test
- Reusable functions across handlers

**Example:**
```python
# handler calls service
user_data = await get_user_profile(telegram_id)

# service handles ORM + data transformation
async def get_user_profile(telegram_id):
    user = await sync_to_async(TelegramUser.objects.get)(telegram_id=telegram_id)
    active_referrals = await sync_to_async(user.referrals.filter)(active=True).count()
    return {
        "username": user.username,
        "referrals": active_referrals
    }
```

---

### 3. **Django ORM for Data Persistence**

**Why?**
- Type-safe database queries
- Built-in migrations
- Admin panel for manual management
- PostgreSQL support for production

**Models:**
```python
# TelegramUser
- telegram_id (unique, indexed) — primary identifier
- username, first_name — user info
- joined_channel (bool) — subscription status
- created_at — join date

# Referral
- inviter (FK) — who invited
- invited (OneToOne) — invited user (no multi-referrer)
- active (bool) — subscription verified
- created_at — referral date
```

**Constraints:**
- `OneToOneField` on `invited` means each user has max 1 inviter
- Index on `telegram_id` for fast lookups

---

### 4. **Polling Instead of Webhooks**

**Why Polling?**
- ✅ Simpler deployment (no public URL needed)
- ✅ Works behind firewalls/NAT
- ✅ Railway-friendly (worker process, no HTTP binding)
- ❌ Slower updates (30-45s latency)
- ❌ Higher bandwidth usage

**Implementation:**
```python
# bot/main.py
await bot.delete_webhook(drop_pending_updates=True)
await dp.start_polling(bot)  # Telegram update polling loop
```

---

### 5. **Single-Referrer Constraint**

**Current:**
```python
invited = models.OneToOneField(TelegramUser, on_delete=models.CASCADE)
```

**Why?**
- Simplifies leaderboard logic
- Clear chain: inviter → invitee

**Limitation:**
- User can only have 1 inviter
- If you need multi-source tracking, change to `ForeignKey` + composite key

---

## Data Flow Examples

### Example 1: User Starts Bot with Referral Link

```
1. Telegram: /start?start=USER_ID
2. Handler: start.py
   ├─ Extract referral param (USER_ID)
   ├─ Call: get_or_create_user(telegram_id)
   ├─ Call: create_referral(inviter_id=USER_ID, invited_id=telegram_id)
   ├─ Call: send_subscribe_keyboard()
3. Service: users.py
   ├─ Query: TelegramUser.objects.get_or_create(telegram_id=...)
   ├─ Query: Referral.objects.create(inviter_id, invited_id)
4. Database: PostgreSQL/SQLite
   ├─ INSERT INTO referrals_telegramuser(...)
   ├─ INSERT INTO referrals_referral(...)
5. Bot: Send inline keyboard with subscribe button
```

### Example 2: User Verifies Subscription

```
1. User clicks "✅ I've subscribed" button
2. Handler: subscription.py
   ├─ Call: check_subscription(telegram_id)
   ├─ If verified:
   │  ├─ Call: activate_referral(invited_id=telegram_id)
   │  ├─ Send: personal referral link
   │  └─ Send: welcome message
3. Service: subscriptions.py
   ├─ API call: bot.get_chat_member(CHANNEL_ID, telegram_id)
   ├─ Check: member.status in ['member', 'creator', 'administrator']
   ├─ If true:
   │  └─ Query: Referral.objects.filter(invited=telegram_id).update(active=True)
4. Database: PostgreSQL/SQLite
   ├─ UPDATE referrals_referral SET active=TRUE
5. Bot: Send success message with referral link
```

### Example 3: User Views Profile

```
1. User: /profile
2. Handler: profile.py
   ├─ Call: get_user_profile(telegram_id)
3. Service: users.py
   ├─ Query: TelegramUser.objects.get(telegram_id)
   ├─ Query: Referral.objects.filter(inviter_id, active=True).count()
   ├─ Query: user.invited_by (if exists)
4. Database: PostgreSQL/SQLite
   ├─ SELECT FROM referrals_telegramuser WHERE telegram_id=...
   ├─ SELECT COUNT(*) FROM referrals_referral WHERE inviter_id=... AND active=TRUE
5. Bot: Send formatted message with stats
```

---

## Performance Considerations

### Database Indexing

Current indexes (from models):
- `TelegramUser.telegram_id` — `unique=True, db_index=True`

**Recommended additional indexes:**
```python
class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    joined_channel = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

class Referral(models.Model):
    inviter = models.ForeignKey(..., db_index=True)
    active = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

### Query Optimization

**Current patterns:**
```python
# ✅ Good: filtered query with count
user.referrals.filter(active=True).count()

# ⚠️ Watch out: N+1 queries (each user → separate query)
for user in TelegramUser.objects.all():
    print(user.referrals.count())  # Adds query per user
```

**Optimized:**
```python
from django.db.models import Count

# ✅ Annotate: single query with count
users = TelegramUser.objects.annotate(
    active_referrals=Count('referrals', filter=Q(referrals__active=True))
)
```

---

## Deployment Architecture

### Local Development
```
Python 3.9+ → aiogram → Django → SQLite → process
```

### Production (Railway)
```
Git Push → Railway Webhook → Docker Build
    ↓
    └─→ Run: ./start.sh
        └─→ python manage.py migrate
        └─→ python bot/main.py
                ↓
            Polling loop
                ↓
        PostgreSQL (Railway Postgres)
```

**Why Railway?**
- One-click GitHub integration
- Managed PostgreSQL
- Easy environment variables
- Free tier available
- No container knowledge required

---

## Testing Strategy

### Unit Tests (Recommended)

```python
# referrals/tests.py
from django.test import TestCase
from referrals.models import TelegramUser, Referral

class TelegramUserTestCase(TestCase):
    def test_user_creation(self):
        user = TelegramUser.objects.create(telegram_id=123456789)
        self.assertEqual(user.telegram_id, 123456789)
        self.assertFalse(user.joined_channel)

class ReferralTestCase(TestCase):
    def test_referral_creation(self):
        inviter = TelegramUser.objects.create(telegram_id=111)
        invited = TelegramUser.objects.create(telegram_id=222)
        ref = Referral.objects.create(inviter=inviter, invited=invited)
        self.assertFalse(ref.active)

    def test_activate_referral(self):
        # ... test activation logic
```

### Integration Tests (Future)

```python
# Test handler → service → database flow
async def test_start_handler_with_referral():
    # Mock Telegram update
    # Run handler
    # Assert database state changed
```

---

## Future Improvements

### 1. Switch to Webhooks

**Why:**
- Real-time updates (vs 30s polling)
- Lower bandwidth
- Railway support via custom domain

**Cost:**
- Need public HTTPS URL
- Webhook IP validation
- Error handling for delivery failures

### 2. Add Caching

```python
from django.core.cache import cache

# Cache leaderboard (recompute every 1 hour)
leaderboard = cache.get('leaderboard_top10')
if not leaderboard:
    leaderboard = Referral.objects.filter(active=True).values('inviter').annotate(...)
    cache.set('leaderboard_top10', leaderboard, 3600)
```

### 3. Rate Limiting

```python
# Prevent spam
from django.core.cache import cache

def rate_limit(user_id, limit=10, window=60):  # 10 commands per 60 seconds
    key = f"rate_limit:{user_id}"
    count = cache.get(key, 0)
    if count >= limit:
        return False
    cache.set(key, count + 1, window)
    return True
```

### 4. Logging & Monitoring

```python
import logging

logger = logging.getLogger(__name__)

async def start_handler(message: Message):
    logger.info(f"User {message.from_user.id} started bot")
    # ... rest of logic
```

---

## Conclusion

This architecture balances **simplicity** (polling, SQLite) with **scalability** (PostgreSQL, async). It's ideal for:
- ✅ Pet projects & MVPs
- ✅ Small-to-medium user bases (~10k users)
- ✅ Learning Django + aiogram

For larger scale (100k+ users), consider:
- Webhook over polling
- Redis caching
- Database read replicas
- Rate limiting & queue system (Celery)
