# 🚀 MIDAS BOT - Automated Task Handler

MIDAS BOT adalah skrip otomatisasi yang membantu kamu menyelesaikan berbagai tugas di platform MidasRWA, seperti login, check-in harian, bermain game, dan klaim tugas.  
Skrip ini mendukung penggunaan **proxy otomatis** untuk menghindari pembatasan IP.

## 🎯 Fitur
✅ **Otomatisasi tugas** → Login, check-in harian, bermain game, dan klaim tugas  
✅ **Progress bar** → Menampilkan progres akun yang sedang diproses  
✅ **Log rapi & profesional** → Format log lebih jelas dan mudah dibaca  
✅ **Dukungan proxy otomatis** → Bisa menggunakan **proxy.txt** (jika tersedia)  
✅ **Loop tanpa henti** → Skrip berjalan terus-menerus untuk memproses akun  

---

## 📦 Instalasi

### **1️⃣ Clone Repository**
```bash
git clone https://github.com/Yuurichan-N3/Midas-Yielder.git
cd Midas-Yielder
```

2️⃣ Instal Dependensi

```bash
pip install -r requirements.txt
```

3️⃣ Jalankan Skrip

```bash
python bot.py
```

---

⚙️ Konfigurasi Proxy (Opsional)

Jika ingin menggunakan proxy, buat file proxy.txt dan tambahkan daftar proxy (satu per baris).

Jika proxy.txt kosong, skrip akan berjalan tanpa proxy.


📌 Contoh format proxy.txt:

http://user:pass@proxyserver:port
socks5://proxyserver:port


---

📂 Struktur File

📁 midas-bot
 ├── bot.py            # Skrip utama
 ├── requirements.txt    # Dependensi yang harus diinstal
 ├── data.txt         # Daftar akun (wajib diisi)
 ├── proxy.txt           # Daftar proxy (opsional)
 ├── README.md           # Dokumentasi proyek


---

📝 Catatan

Pastikan file data.txt berisi query yang akan diproses.

Jika ada akun yang gagal login, skrip tetap berjalan untuk akun lainnya.



---

📜 Lisensi

MIT License
