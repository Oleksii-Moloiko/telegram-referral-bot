# Telegram Referral Bot

Telegram referral bot built with Python, aiogram, and Django.

The bot allows users to generate referral links, invite other users, verify Telegram channel subscription, and track active referrals through Django Admin.

## Features

- Telegram bot with aiogram
- Django database models for users and referrals
- Referral link generation
- Referral tracking via `/start` parameter
- Telegram channel subscription verification
- Active referral counting
- User profile command
- Reply keyboard menu
- Django Admin panel

## Tech Stack

- Python
- aiogram
- Django
- SQLite for local development
- python-dotenv

## Project Structure

```text
telegram-referral-bot/
├── bot/
│   ├── handlers/
│   │   ├── start.py
│   │   ├── profile.py
│   │   ├── subscription.py
│   │   └── help.py
│   ├── keyboards/
│   │   └── menu.py
│   ├── services/
│   │   ├── users.py
│   │   ├── messages.py
│   │   └── subscriptions.py
│   └── main.py
├── referrals/
│   ├── models.py
│   └── admin.py
├── config/
├── manage.py
├── .env.example
├── .gitignore
└── requirements.txt
```

## Setup

Clone the repository:

```bash
git clone <repository-url>
cd telegram-referral-bot
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create .env from example:

```bas
cp .env.example .env
```

Fill in your environment variables:

```env
BOT_TOKEN=your_bot_token_here
BOT_USERNAME=your_bot_username_here
CHANNEL_ID=@your_channel_username
CHANNEL_URL=https://t.me/your_channel_username
SECRET_KEY=your_django_secret_key_here
DEBUG=True
```

Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Create Django admin user:

```bash
python manage.py createsuperuser
```

Run Django admin:

```bash
python manage.py runserver
```

Run the Telegram bot in a separate terminal:

```bash
python bot/main.py
```

---

## Telegram Setup

1. Create a bot via BotFather.
2. Add the bot token to .env.
3. Create a Telegram channel.
4. Add the bot as an administrator of the channel.
5. Add channel username to CHANNEL_ID.
6. Add public channel link to CHANNEL_URL.

---

## Bot Commands

```
/start - start the bot and process referral links
/profile - show user profile and referral stats
/help - show help message
```

---

## Referral Flow

1. User starts the bot.
2. Bot creates a user record.
3. Bot gives instructions to subscribe to the channel.
4. User verifies subscription.
5. Bot activates the user referral if the user joined through a referral link.
6. User receives a personal referral link.
7. Active referrals are counted only after subscription verification.

---

## Environment Variables

| Variable       | Description                        |
| -------------- | ---------------------------------- |
| `BOT_TOKEN`    | Telegram bot token from BotFather  |
| `BOT_USERNAME` | Bot username without `@`           |
| `CHANNEL_ID`   | Telegram channel username with `@` |
| `CHANNEL_URL`  | Public Telegram channel URL        |
| `SECRET_KEY`   | Django secret key                  |
| `DEBUG`        | Django debug mode                  |

---

## Admin Panel

Django Admin is available at:

```
http://127.0.0.1:8000/admin/
```

You can manage:

- Telegram users
- Referrals
- Referral active status
- Subscription status