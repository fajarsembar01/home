# 🏠 Property Collection Bot

Bot Telegram AI untuk mengumpulkan dan mengelola data properti menggunakan **Google Gemini AI** (gemini-1.5-flash) dan **PostgreSQL**.

## ✨ Fitur

- 🤖 **AI-Powered**: Ekstraksi data properti otomatis dari natural language menggunakan Gemini 1.5 Flash
- 💬 **Chat Interface**: Interaksi mudah melalui Telegram
- 🗄️ **Database PostgreSQL**: Penyimpanan data terstruktur dan aman
- 📸 **Photo Support**: Upload dan simpan foto properti
- 📊 **Statistics**: Lihat statistik dan ringkasan properti
- 🆓 **Completely Free**: Menggunakan API gratis (Gemini, Telegram)

## 📋 Prasyarat

- Python 3.9 atau lebih tinggi
- PostgreSQL database (lokal atau cloud seperti ElephantSQL)
- Akun Telegram
- Google Gemini API Key (gratis)

## 🚀 Instalasi

### 1. Clone atau Download Project

```bash
cd "AI properti"
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Database

**Opsi A: PostgreSQL Lokal**

1. Install PostgreSQL di komputer Anda
2. Buat database baru:
```bash
createdb properti_db
```
3. Jalankan schema:
```bash
psql -d properti_db -f schema.sql
```

**Opsi B: ElephantSQL (Cloud - Gratis)**

1. Daftar di https://www.elephantsql.com/
2. Buat instance baru (plan Tiny Turtle - gratis)
3. Copy connection URL
4. Gunakan URL tersebut di file `.env`

### 4. Dapatkan Telegram Bot Token

1. Buka Telegram, cari **@BotFather**
2. Kirim perintah `/newbot`
3. Ikuti instruksi (berikan nama dan username bot)
4. Copy token yang diberikan (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 5. Dapatkan Gemini API Key

1. Buka https://aistudio.google.com/app/apikey
2. Login dengan akun Google
3. Klik **"Create API Key"**
4. Copy API key yang diberikan

### 6. Konfigurasi Environment Variables

1. Copy file `.env.example` menjadi `.env`:
```bash
cp .env.example .env
```

2. Edit file `.env` dan isi dengan credentials Anda:
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://username:password@host:port/database
```

**Contoh DATABASE_URL:**
- Lokal: `postgresql://postgres:mypassword@localhost:5432/properti_db`
- ElephantSQL: `postgresql://username:password@hostname/database`

## ▶️ Menjalankan Bot

```bash
python bot.py
```

Jika berhasil, Anda akan melihat:
```
INFO - Initializing database...
INFO - Database tables created successfully
INFO - Bot started successfully! Press Ctrl+C to stop.
```

## 📱 Cara Menggunakan

### 1. Mulai Bot

- Buka Telegram
- Cari username bot Anda (yang dibuat di BotFather)
- Kirim `/start`

### 2. Tambah Properti Baru

Kirim `/add` atau langsung ketik deskripsi properti secara natural:

**Contoh:**
```
Rumah 2 lantai di Menteng Jakarta Pusat, 4 kamar tidur, 3 kamar mandi, 
luas tanah 200m², luas bangunan 300m², harga 5 miliar nego, 
sertifikat SHM, ada kolam renang dan taman
```

Bot akan:
1. Mengekstrak semua informasi menggunakan AI
2. Menampilkan ringkasan untuk konfirmasi
3. Menyimpan ke database setelah Anda approve
4. Menawarkan untuk upload foto

### 3. Lihat Properti

Kirim `/list` untuk melihat semua properti yang telah ditambahkan.

### 4. Statistik

Kirim `/stats` untuk melihat ringkasan dan statistik properti.

### 5. Bantuan

Kirim `/help` untuk melihat panduan lengkap.

## 📊 Struktur Database

### Tabel `users`
- Menyimpan data user Telegram

### Tabel `properties`
- Jenis properti (rumah, apartemen, tanah, dll)
- Lokasi lengkap
- Harga dan tipe transaksi (jual/sewa)
- Luas tanah & bangunan
- Spesifikasi (kamar, lantai, dll)
- Fasilitas
- Kontak
- Sertifikat

### Tabel `property_images`
- Multiple foto per properti
- Storage menggunakan Telegram file_id

## 🤖 AI Processing

Bot menggunakan **Google Gemini 1.5 Flash** yang:
- ✅ **Gratis** dengan rate limit tinggi (15 req/menit)
- ✅ Mendukung **function calling** untuk data terstruktur
- ✅ Akurat dalam ekstraksi informasi dari bahasa natural
- ✅ Fallback parser untuk handling edge cases

## 🛠️ Troubleshooting

### Error: "TELEGRAM_BOT_TOKEN not found"
- Pastikan file `.env` ada dan berisi token yang benar
- Cek format token (harus dari @BotFather)

### Error: "GEMINI_API_KEY not found"
- Pastikan API key sudah di-set di `.env`
- Verifikasi API key valid di Google AI Studio

### Error: Database connection failed
- Cek kredensial PostgreSQL di `DATABASE_URL`
- Pastikan PostgreSQL service berjalan
- Test koneksi manual dengan `psql`

### Bot tidak merespon
- Pastikan bot sedang berjalan (`python bot.py`)
- Cek log error di terminal
- Restart bot jika perlu

## 📝 Development

### File Structure
```
AI properti/
├── bot.py              # Main bot application
├── database.py         # Database ORM and CRUD
├── ai_processor.py     # Gemini AI integration
├── requirements.txt    # Python dependencies
├── schema.sql         # Database schema
├── .env               # Environment variables (gitignored)
├── .env.example       # Template untuk .env
└── README.md          # Dokumentasi ini
```

### Extend Functionality

**Menambah field properti baru:**
1. Update `schema.sql` dengan kolom baru
2. Update ORM model di `database.py`
3. Update function calling schema di `ai_processor.py`
4. Migrate database

**Menambah command baru:**
1. Buat handler function di `bot.py`
2. Register dengan `application.add_handler()`

## 🔒 Keamanan

- ✅ `.env` di-gitignore untuk keamanan credentials
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ Input validation di AI processor
- ✅ User isolation (setiap user hanya lihat properti sendiri)

## 📞 Support

Butuh bantuan? Hubungi developer atau buat issue di repository.

## 📄 License

MIT License - Free to use and modify

---

**Dibuat dengan ❤️ menggunakan:**
- [python-telegram-bot](https://python-telegram-bot.org/)
- [Google Gemini AI](https://ai.google.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
