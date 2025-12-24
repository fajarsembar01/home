# 🚀 Quick Start Guide - Property Collection Bot

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] PostgreSQL installed (or ElephantSQL account)
- [ ] Telegram account
- [ ] Google account (for Gemini API)

## 5-Minute Setup

### Step 1: Get Telegram Bot Token (2 min)
1. Open Telegram, search: `@BotFather`
2. Send: `/newbot`
3. Follow instructions (choose name and username)
4. **Copy the token** (looks like: `123456789:ABCdefGHI...`)

### Step 2: Get Gemini API Key (2 min)
1. Visit: https://aistudio.google.com/app/apikey
2. Click: **"Create API Key"**
3. **Copy the API key**

### Step 3: Setup Database (1 min)

**Option A - Local PostgreSQL:**
```bash
createdb properti_db
psql -d properti_db -f schema.sql
```

**Option B - ElephantSQL (Cloud - Free):**
1. Sign up at https://www.elephantsql.com/
2. Create new instance (Tiny Turtle plan - FREE)
3. Copy connection URL

### Step 4: Configure & Run
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
# (Add the tokens and database URL you got from steps 1-3)

# Install dependencies
pip3 install -r requirements.txt

# Test setup
python3 test_setup.py

# Run the bot!
python3 bot.py
```

## Using the Bot

### 1. Find Your Bot
Open Telegram → Search for your bot username → Click START

### 2. Add Property
Send this example:
```
Rumah 2 lantai di Jakarta Selatan, 3 kamar tidur, 
2 kamar mandi, luas tanah 100m², harga 2 miliar nego
```

Bot will extract all data automatically! ✨

### 3. View Properties
```
/list  → See all properties
/stats → View statistics
/help  → Get help
```

## Troubleshooting

### "Bot not responding"
- Check if `python3 bot.py` is running
- Verify `TELEGRAM_BOT_TOKEN` in `.env`

### "Database connection failed"
- Check `DATABASE_URL` in `.env`
- Verify PostgreSQL is running: `psql -l`

### "Gemini API error"
- Verify `GEMINI_API_KEY` in `.env`
- Check quota at https://aistudio.google.com

## Environment Variables Format

```bash
# .env file example
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
GEMINI_API_KEY=AIzaSyA1B2C3D4E5F6G7H8I9J0K
DATABASE_URL=postgresql://postgres:mypass@localhost:5432/properti_db
```

## Testing

Run the test suite:
```bash
python3 test_setup.py
```

Should show:
```
✅ PASS - Environment
✅ PASS - Database
✅ PASS - Gemini AI
🎉 All tests passed!
```

## Need Help?

1. Check [README.md](README.md) for detailed documentation
2. Review logs when running `python3 bot.py`
3. Make sure all prerequisites are installed

---

**That's it! You're ready to collect property data with AI! 🏠🤖**
