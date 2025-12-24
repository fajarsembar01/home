# Gemini API Free Tier Quota Information

## Current Status
⚠️ **API Quota sudah terpakai** dari testing sebelumnya

## Solusi yang Sudah Diterapkan

### 1. Gunakan Model Lite
Bot sekarang menggunakan `gemini-flash-lite-latest` yang lebih hemat quota:
- ✅ Request lebih kecil (token lebih sedikit)
- ✅ Response lebih cepat
- ✅ Quota dipakai lebih sedikit per request

### 2. Fallback Parser
Jika AI quota habis, bot otomatis menggunakan regex parser:
- ✅ Tetap bisa ekstrak data dasar (tipe, harga, kamar)
- ✅ Tidak bergantung 100% pada API
- ✅ User tetap bisa input properti

## Quota Limits (Free Tier)

### Per Minute
- Requests: 15 RPM
- Input tokens: 1 juta tokens/min

### Per Day
- Requests: 1,500 per day
- Input tokens: 1 juta tokens/day

## Cara Mengatasi Quota Habis

### Opsi 1: Tunggu Reset (Otomatis)
Quota akan reset:
- **Per-minute quota**: Reset setiap 60 detik
- **Daily quota**: Reset setiap 24 jam (tengah malam PST)

### Opsi 2: Buat API Key Baru
1. Buka https://aistudio.google.com/app/apikey
2. Login dengan **akun Google berbeda**
3. Create API Key baru
4. Update di file `.env`:
   ```
   GEMINI_API_KEY=your_new_api_key_here
   ```

### Opsi 3: Gunakan Fallback Parser Saja
Bot sudah didesain untuk tetap bekerja tanpa AI:
- User tetap bisa input properti
- Regex parser akan ekstrak data dasar
- Konfirmasi manual oleh user

## Testing Best Practices

Untuk menghindari quota habis saat testing:

1. **Batasi Test Calls**
   ```python
   # Di test_setup.py, hanya test 1x saja
   # Jangan loop atau retry berkali-kali
   ```

2. **Gunakan Cache**
   Simpan hasil ekstraksi untuk input yang sama

3. **Mock Responses**
   Untuk development, mock Gemini response

## Monitoring Quota

Cek penggunaan quota Anda:
- https://ai.google.dev/gemini-api/docs/quota
- https://aistudio.google.com/app/apikey (lihat usage)

## Model Alternatif (Jika Perlu)

Jika tetap ada masalah, bisa gunakan:
- ❌ ~~gemini-2.0-flash~~ (quota lebih ketat)
- ✅ **gemini-flash-lite-latest** (CURRENT - paling hemat)
- ✅ gemini-1.5-flash-001 (alternatif)

---

**Status Saat Ini**: Bot menggunakan `gemini-flash-lite-latest` + fallback parser yang robust ✅
