# 🚀 Panduan Deploy Bot Properti ke VPS

Panduan lengkap untuk deploy Telegram Property Bot dengan AI ke VPS Ubuntu/Debian.

## 📋 Prerequisites

- VPS dengan Ubuntu 20.04+ atau Debian 11+
- Python 3.9 atau lebih baru
- PostgreSQL 13+
- Akses SSH ke VPS
- Domain (opsional, untuk SSL)

---

## 🔧 Langkah 1: Persiapan VPS

### 1.1 Login ke VPS
```bash
ssh root@your-vps-ip
# atau
ssh your-username@your-vps-ip
```

### 1.2 Update Sistem
```bash
sudo apt update && sudo apt upgrade -y
```

### 1.3 Install Dependencies
```bash
# Install Python 3 dan pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install git
sudo apt install git -y

# Install tools tambahan
sudo apt install curl wget nano htop -y
```

---

## 🗄️ Langkah 2: Setup Database PostgreSQL

### 2.1 Masuk ke PostgreSQL
```bash
sudo -u postgres psql
```

### 2.2 Buat Database dan User
```sql
-- Buat database
CREATE DATABASE properti_db;

-- Buat user (ganti 'your_password' dengan password kuat)
CREATE USER properti_user WITH PASSWORD 'your_password';

-- Berikan privileges
GRANT ALL PRIVILEGES ON DATABASE properti_db TO properti_user;

-- Keluar
\q
```

### 2.3 Test Koneksi Database
```bash
psql -U properti_user -d properti_db -h localhost
# Masukkan password yang sudah dibuat
# Jika berhasil, keluar dengan: \q
```

---

## 📦 Langkah 3: Clone Repository

### 3.1 Buat Direktori untuk Aplikasi
```bash
cd /opt
sudo mkdir telegram-bot
sudo chown $USER:$USER telegram-bot
cd telegram-bot
```

### 3.2 Clone dari GitHub
```bash
git clone https://github.com/fajarsembar01/home.git .
```

### 3.3 Verifikasi File
```bash
ls -la
# Harus ada: bot.py, database.py, requirements.txt, dll
```

---

## 🔐 Langkah 4: Konfigurasi Environment

### 4.1 Buat File .env
```bash
cp .env.example .env
nano .env
```

### 4.2 Edit File .env
Isi dengan kredensial yang benar:

```env
# Telegram Bot Token dari @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# Gemini API Key dari https://aistudio.google.com/app/apikey
GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Database URL (sesuaikan dengan user & password yang dibuat)
DATABASE_URL=postgresql://properti_user:your_password@localhost:5432/properti_db

# Logging
LOG_LEVEL=INFO
```

**Cara mendapatkan kredensial:**

#### Telegram Bot Token:
1. Buka Telegram, cari `@BotFather`
2. Kirim `/newbot`
3. Ikuti instruksi (nama bot & username)
4. Copy token yang diberikan

#### Gemini API Key:
1. Buka https://aistudio.google.com/app/apikey
2. Login dengan Google Account
3. Klik "Create API Key"
4. Copy API key yang dihasilkan

Simpan file dengan `Ctrl + O`, `Enter`, lalu `Ctrl + X`

---

## 🐍 Langkah 5: Setup Python Environment

### 5.1 Buat Virtual Environment
```bash
python3 -m venv venv
```

### 5.2 Aktifkan Virtual Environment
```bash
source venv/bin/activate
```

### 5.3 Install Python Packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5.4 Verifikasi Instalasi
```bash
pip list
# Harus ada: python-telegram-bot, google-genai, psycopg2-binary, dll
```

---

## 🗃️ Langkah 6: Inisialisasi Database

### 6.1 Jalankan Schema SQL
```bash
psql -U properti_user -d properti_db -h localhost -f schema.sql
# Masukkan password database
```

### 6.2 (Opsional) Load Data Contoh
```bash
python3 seed_data.py
```

### 6.3 Verifikasi Tabel
```bash
psql -U properti_user -d properti_db -h localhost
```

```sql
-- List semua tabel
\dt

-- Harus ada tabel: properties, users, dll
-- Keluar
\q
```

---

## 🚀 Langkah 7: Test Bot

### 7.1 Test Run Manual
```bash
# Pastikan venv aktif
source venv/bin/activate

# Jalankan bot
python3 bot.py
```

Jika berhasil, Anda akan melihat:
```
🏠 Property Bot is starting...
✓ Database connected successfully
✓ Bot started! Press Ctrl-C to stop.
```

**Test di Telegram:**
1. Buka Telegram, cari bot Anda
2. Kirim `/start`
3. Test upload foto properti

Jika berfungsi dengan baik, tekan `Ctrl + C` untuk stop, lalu lanjut ke setup systemd.

---

## ⚙️ Langkah 8: Setup Systemd Service (Auto-Start)

### 8.1 Buat Service File
```bash
sudo nano /etc/systemd/system/telegram-properti-bot.service
```

### 8.2 Paste Konfigurasi Ini
```ini
[Unit]
Description=Telegram Property Bot with AI
After=network.target postgresql.service

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/opt/telegram-bot
Environment="PATH=/opt/telegram-bot/venv/bin"
ExecStart=/opt/telegram-bot/venv/bin/python3 /opt/telegram-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Ganti `YOUR_USERNAME`** dengan username Linux Anda:
```bash
whoami  # untuk melihat username
```

Simpan dengan `Ctrl + O`, `Enter`, lalu `Ctrl + X`

### 8.3 Enable dan Start Service
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable auto-start saat boot
sudo systemctl enable telegram-properti-bot

# Start service
sudo systemctl start telegram-properti-bot

# Check status
sudo systemctl status telegram-properti-bot
```

Jika berhasil, status akan menunjukkan **active (running)** dengan warna hijau.

### 8.4 Perintah untuk Manage Service
```bash
# Start bot
sudo systemctl start telegram-properti-bot

# Stop bot
sudo systemctl stop telegram-properti-bot

# Restart bot
sudo systemctl restart telegram-properti-bot

# Check status
sudo systemctl status telegram-properti-bot

# Lihat log
sudo journalctl -u telegram-properti-bot -f
```

---

## 📊 Langkah 9: Monitoring & Troubleshooting

### 9.1 Lihat Log Real-time
```bash
sudo journalctl -u telegram-properti-bot -f
```

### 9.2 Lihat 100 Log Terakhir
```bash
sudo journalctl -u telegram-properti-bot -n 100
```

### 9.3 Check Resource Usage
```bash
htop
# Cari proses "python3 bot.py"
# Tekan 'q' untuk keluar
```

### 9.4 Troubleshooting Umum

#### Bot tidak start?
```bash
# Check status detail
sudo systemctl status telegram-properti-bot

# Check log error
sudo journalctl -u telegram-properti-bot -n 50

# Periksa .env file
cat .env

# Test manual untuk debug
cd /opt/telegram-bot
source venv/bin/activate
python3 bot.py
```

#### Database connection error?
```bash
# Test koneksi PostgreSQL
psql -U properti_user -d properti_db -h localhost

# Check PostgreSQL status
sudo systemctl status postgresql

# Restart PostgreSQL
sudo systemctl restart postgresql
```

#### Import error / module not found?
```bash
# Reinstall dependencies
cd /opt/telegram-bot
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

---

## 🔄 Langkah 10: Update Bot (Git Pull)

Ketika ada update kode:

```bash
# Stop bot
sudo systemctl stop telegram-properti-bot

# Pull update dari GitHub
cd /opt/telegram-bot
git pull origin main

# Update dependencies (jika ada perubahan)
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Restart bot
sudo systemctl start telegram-properti-bot

# Check status
sudo systemctl status telegram-properti-bot
```

---

## 🔒 Langkah 11: Security Best Practices

### 11.1 Setup Firewall
```bash
# Install UFW
sudo apt install ufw -y

# Allow SSH (PENTING! Jangan sampai terkunci)
sudo ufw allow ssh

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 11.2 Ganti Port SSH (Opsional)
```bash
sudo nano /etc/ssh/sshd_config
# Ganti: Port 22 -> Port 2222 (atau port lain)
# Simpan dan restart SSH
sudo systemctl restart sshd

# JANGAN LUPA allow port baru di firewall:
sudo ufw allow 2222
```

### 11.3 Disable Root Login (Opsional)
```bash
sudo nano /etc/ssh/sshd_config
# Ganti: PermitRootLogin yes -> PermitRootLogin no
# Simpan dan restart SSH
sudo systemctl restart sshd
```

### 11.4 Backup Database Rutin

Buat script backup:
```bash
nano /opt/telegram-bot/backup.sh
```

Paste script ini:
```bash
#!/bin/bash
BACKUP_DIR="/opt/telegram-bot/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U properti_user -d properti_db > $BACKUP_DIR/properti_db_$DATE.sql
# Hapus backup lebih dari 7 hari
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

Buat executable dan test:
```bash
chmod +x /opt/telegram-bot/backup.sh
./backup.sh
```

Setup cron job untuk backup otomatis setiap hari jam 2 pagi:
```bash
crontab -e
```

Tambahkan baris ini:
```
0 2 * * * /opt/telegram-bot/backup.sh
```

---

## ✅ Checklist Deploy

- [ ] VPS sudah update
- [ ] Python 3.9+ terinstall
- [ ] PostgreSQL terinstall dan running
- [ ] Database & user sudah dibuat
- [ ] Repository sudah di-clone
- [ ] File .env sudah dikonfigurasi dengan benar
- [ ] Virtual environment sudah dibuat
- [ ] Dependencies sudah terinstall
- [ ] Database schema sudah dijalankan
- [ ] Bot sudah test manual dan berfungsi
- [ ] Systemd service sudah dikonfigurasi
- [ ] Bot running sebagai service dan auto-start
- [ ] Firewall sudah dikonfigurasi
- [ ] Backup script sudah dibuat

---

## 📞 Support

Jika ada masalah:

1. **Check log**: `sudo journalctl -u telegram-properti-bot -f`
2. **Test manual**: Jalankan bot langsung dengan `python3 bot.py`
3. **Periksa .env**: Pastikan semua kredensial benar
4. **Check database**: Test koneksi PostgreSQL
5. **Restart service**: `sudo systemctl restart telegram-properti-bot`

---

## 📚 Resource Tambahan

- [Python Telegram Bot Docs](https://docs.python-telegram-bot.org/)
- [Google Gemini AI Docs](https://ai.google.dev/docs)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Systemd Service Docs](https://www.freedesktop.org/software/systemd/man/systemd.service.html)

---

**Happy Deploying! 🎉**
