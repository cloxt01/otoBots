# Dokumentasi OtoBot: Agen Otonom Multi-Tujuan

## Pendahuluan

OtoBot adalah sebuah sistem agen otonom yang dirancang untuk beroperasi sepenuhnya secara mandiri, tanpa memerlukan campur tangan manusia setelah konfigurasi awal. Bot ini dibangun untuk mencapai tujuan yang telah ditetapkan, menjadikannya solusi ideal untuk otomatisasi tugas yang kompleks dan berkelanjutan. Fleksibilitas dalam konfigurasinya memungkinkan adaptasi mudah terhadap berbagai skenario penggunaan.

## Apa Itu OtoBot?

OtoBot adalah sebuah bot otonom yang mampu mengeksekusi serangkaian tindakan dan mencapai objektif spesifik secara otomatis. Kemampuan intinya terletak pada kemandirian operasionalnya, yang menghilangkan kebutuhan akan intervensi manual berkelanjutan. Ini membebaskan sumber daya manusia dan memastikan efisiensi tinggi dalam tugas-tugas yang repetitif atau berbasis waktu.

## Fitur Utama

- **Otonomi Penuh**: Beroperasi dan membuat keputusan secara mandiri untuk mencapai tujuan yang telah ditetapkan.
- **Konfigurasi Tujuan**: Tujuan dan perilaku bot dapat diatur secara detail melalui file konfigurasi `conf/conf.json`.
- **Modular**: Dibangun dengan struktur modular yang jelas, memisahkan fungsionalitas inti ke dalam komponen-komponen yang terdefinisi.
- **Fleksibel**: Dapat diadaptasi untuk berbagai kasus penggunaan berkat sistem konfigurasinya yang kuat.

## Struktur Proyek dan Peran Komponen

Proyek OtoBot tersusun secara modular, dengan setiap direktori mewakili bagian fungsional yang berbeda. Struktur ini dirancang untuk memudahkan pengembangan, debugging, dan pemeliharaan.

.
├── .idea/ # (Opsional) Direktori konfigurasi IDE (mis. PyCharm)
├── conf/ # Konfigurasi Bot
├── content/ # Direktori Output Utama
├── generator/ # Modul Generator Output
├── log/ # Pencatatan (Logging)
├── processor/ # Modul Pemrosesan Data
├── runner/ # Eksekutor File/Tugas
├── sniffer/ # Penangkapan Lalu Lintas Jaringan
├── .gitignore # File yang diabaikan oleh Git
└── main.py # Titik Masuk Utama Aplikasi

shell
Salin
Edit

### `/conf`

Direktori ini adalah pusat kendali untuk perilaku OtoBot. Berisi file konfigurasi, terutama `conf.json`, di mana Anda menentukan tujuan bot, parameter operasional, dan pengaturan lainnya. Perubahan di sini akan langsung memengaruhi bagaimana bot beroperasi.

### `/content`

Ini adalah direktori output utama dari OtoBot. Semua data, laporan, atau file lain yang dihasilkan atau dimanipulasi oleh bot selama operasinya akan disimpan di sini.

### `/generator`

Modul-modul di dalam direktori ini bertanggung jawab untuk menghasilkan atau meminta output awal yang kemudian akan diproses lebih lanjut.

### `/log`

Direktori ini didedikasikan untuk pencatatan aktivitas OtoBot. Semua event penting seperti error, status operasi, dan informasi debugging disimpan dalam file log di sini.

### `/processor`

Berisi logika untuk memproses data output dari generator, seperti analisis, transformasi, filtering, atau normalisasi.

### `/runner`

Modul ini bertanggung jawab untuk menjalankan file atau tugas yang telah disimpan di `/content`, seperti eksekusi skrip, peluncuran proses, atau aktivasi fungsi.

### `/sniffer`

Berfungsi untuk menangkap lalu lintas jaringan. Informasi yang ditangkap ini bisa digunakan untuk analisis atau pemicu tindakan otomatis.

### `main.py`

Titik masuk utama untuk menjalankan OtoBot. Skrip ini mengoordinasikan semua komponen modular lainnya.

### `.gitignore`

File standar Git yang menentukan file dan direktori mana yang harus diabaikan oleh sistem kontrol versi Git.

## Instalasi (Contoh)

### Kloning Repositori:

```bash
git clone https://github.com/cloxt01/otoBots.git
```

### Instal Dependensi:

```bash
pip install -r requirements.txt
```


Semua konfigurasi utama untuk OtoBot diatur dalam file conf/conf.json. Pastikan untuk mengedit file ini sesuai dengan tujuan dan parameter operasi Anda.

Contoh konfigurasi :

```json
{
  "url": "https://www.tokopedia.com/mongse/minyak-goreng-sania-1-l-43cac",

  "api" : {
    "domain": "gql.tokopedia.com"
  },
  "browser": {
    "headlessMode": false,
    "profilePath": "C:\\Users\\MyBook Hype\\project\\gcloud\\Profiles\\2tekjd15.Cloxt00"
  },
  "cookie": "",
  "path" : {
    "content" : "content/",
    "runner" : "runner/",
    "log": "log/"
  },
  "ai": {
    "platform": "openrouter-ai",
    "maxTokens" : 16000,
    "apiKey": "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"
  }
}
```

### Penggunaan
Setelah instalasi dan konfigurasi, jalankan OtoBot melalui:

```bash
python main.py
```

Bot akan mulai beroperasi sesuai dengan konfigurasi yang telah Anda tetapkan di conf/conf.json.
