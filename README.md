# **OtoBots**


## Pendahuluan

**OtoBot** adalah otoBits versi `open-source`, sebuah sistem agen otonom yang dirancang untuk beroperasi sepenuhnya secara mandiri, tanpa memerlukan campur tangan manusia setelah konfigurasi awal. Bot ini dibangun untuk mencapai tujuan yang telah ditetapkan, menjadikannya solusi ideal untuk otomatisasi tugas yang kompleks dan berkelanjutan. Fleksibilitas dalam konfigurasinya memungkinkan adaptasi mudah terhadap berbagai skenario penggunaan.

### Apa Itu OtoBot?

OtoBot adalah sebuah **bot otonom** yang mampu mengeksekusi serangkaian tindakan dan mencapai objektif spesifik secara otomatis. Kemampuan intinya terletak pada kemandirian operasionalnya, yang menghilangkan kebutuhan akan intervensi manual berkelanjutan. Ini membebaskan sumber daya manusia dan memastikan efisiensi tinggi dalam tugas-tugas yang repetitif atau berbasis waktu.

### Fitur Utama

* **Otonomi Penuh:** Beroperasi dan membuat keputusan secara mandiri untuk mencapai tujuan yang telah ditetapkan.
* **Konfigurasi Tujuan:** Tujuan dan perilaku bot dapat diatur secara detail melalui file konfigurasi `conf/conf.json`.
* **Modular:** Dibangun dengan struktur modular yang jelas, memisahkan fungsionalitas inti ke dalam komponen-komponen yang terdefinisi.
* **Fleksibel:** Dapat diadaptasi untuk berbagai kasus penggunaan berkat sistem konfigurasinya yang kuat.

---

## Struktur Proyek dan Peran Komponen

Proyek OtoBot tersusun secara modular, dengan setiap direktori mewakili bagian fungsional yang berbeda. Struktur ini dirancang untuk memudahkan pengembangan, *debugging*, dan pemeliharaan.

```.
├── .idea/            # (Opsional) Direktori konfigurasi IDE (mis. PyCharm)
├── conf/             # Konfigurasi Bot
├── content/          # Direktori Output Utama
├── generator/        # Modul Generator Output
├── log/              # Pencatatan (Logging)
├── processor/        # Modul Pemrosesan Data
├── runner/           # Eksekutor File/Tugas
├── sniffer/          # Penangkapan Lalu Lintas Jaringan
├── .gitignore        # File yang diabaikan oleh Git
└── main.py           # Titik Masuk Utama Aplikasi
```


Berikut adalah penjelasan detail untuk setiap komponen:

* ### `/conf`
    Direktori ini adalah pusat kendali untuk perilaku OtoBot. Berisi file **konfigurasi bot**, termasuk file **`conf.json`**, tempat Anda menentukan tujuan bot, parameter operasional, dan pengaturan lainnya. Perubahan di sini akan langsung memengaruhi bagaimana bot beroperasi.

* ### `/content`
    Ini adalah direktori **output utama** dari OtoBot. Semua data, laporan, atau file lain yang dihasilkan atau dimanipulasi oleh bot selama operasinya akan disimpan di sini. Ini berfungsi sebagai repositori sentral untuk hasil kerja bot.

* ### `/generator`
    Modul-modul di dalam direktori ini bertanggung jawab untuk **menghasilkan atau meminta output**, kemungkinan melalui *prompt* atau instruksi internal. Ini adalah bagian yang menciptakan data awal atau memicu proses penghasilan informasi.

* ### `/log`
    Direktori ini didedikasikan untuk **pencatatan (logging)** aktivitas OtoBot. Semua *event* penting, seperti *error*, peringatan, status operasi, dan informasi *debugging*, akan dicatat dan disimpan dalam bentuk file log di sini. Ini krusial untuk pemantauan dan analisis pasca-operasi.

* ### `/processor`
    Berisi logika untuk **memproses data output dari `generator`**. Setelah data awal dihasilkan, modul di sini akan mengambil data tersebut dan melakukan berbagai operasi seperti analisis, transformasi, filtering, atau normalisasi untuk mempersiapkannya untuk penggunaan atau penyimpanan lebih lanjut.

* ### `/runner`
    Modul ini bertanggung jawab untuk **menjalankan file atau tugas yang telah disimpan di `/content`**. Ini menunjukkan kemampuan bot untuk tidak hanya menghasilkan data tetapi juga berinteraksi atau bertindak berdasarkan data yang telah diproses dan disimpan. Ini bisa melibatkan eksekusi skrip, peluncuran proses, atau aktivasi fungsi berdasarkan *output* yang ada.

* ### `/sniffer`
    Bagian ini berfungsi untuk **menangkap *traffic* atau lalu lintas jaringan**. `Sniffer` memungkinkan OtoBot untuk memantau, mendengarkan, atau mengintersep paket data yang mengalir dalam jaringan. Informasi yang ditangkap ini kemudian dapat diumpankan ke bagian `processor` untuk analisis lebih lanjut atau untuk memicu tindakan bot.

* ### `main.py`
    Ini adalah **titik masuk utama** untuk menjalankan OtoBot. Ketika Anda menginisiasi bot, Anda akan menjalankan skrip ini, yang kemudian akan mengoordinasikan semua komponen modular lainnya untuk memulai operasi bot sesuai dengan konfigurasi yang ditetapkan.

* ### `.gitignore`
    File standar Git yang menentukan **file dan direktori mana yang harus diabaikan** oleh sistem kontrol versi Git. Ini biasanya mencakup dependensi yang diinstal, file log, atau konfigurasi IDE lokal yang tidak perlu dibagikan dalam repositori.

---

## Memahami Alur Kerja untuk Konfigurasi Efektif

**Penting:** OtoBot masih dalam **tahap pengembangan**. Untuk melakukan konfigurasi yang efektif melalui `conf/conf.json`, **Butuh pemahaman mendalam tentang bagaimana proyek ini bekerja dan bagaimana setiap komponen berinteraksi adalah krusial**. Tanpa konfigurasi yang tepat yang selaras dengan alur kerja internal bot, OtoBot mungkin **tidak akan beroperasi dengan baik dan bahkan dapat menimbulkan *error***.

### Alur Kerja Operasional OtoBot

1.  ### Pengaturan Tujuan Awal (`conf/conf.json`)
    Sebelum OtoBot mulai beroperasi, Anda harus terlebih dahulu **mendefinisikan tujuan utama** dan semua parameter terkait dalam file `conf/conf.json`. File ini adalah fondasi dari semua tindakan bot.

2.  ### Inisiasi (`main.py`)
    Saat Anda menjalankan **`main.py`**, skrip ini akan membaca dan memuat seluruh konfigurasi dari `conf/conf.json`. Berdasarkan parameter yang dimuat, `main.py` kemudian akan menginisialisasi dan mengoordinasikan komponen-komponen lain yang diperlukan.

3.  ### Pengambilan Data / Pemicu Awal (`/sniffer` atau Pemicu `generator`)
    * Jika bot memantau aktivitas eksternal, komponen di **`/sniffer`** akan diaktifkan untuk **menangkap lalu lintas jaringan**.
    * Atau, jika bot perlu menghasilkan data dari awal atau mengambil informasi dari sumber eksternal, `main.py` akan memicu modul di **`/generator`**.

4.  ### Generasi Output Mentah (`/generator`)
    Modul-modul di **`/generator`** akan bekerja berdasarkan instruksi untuk **menghasilkan output awal atau data mentah**.

5.  ### Pemrosesan Data (`/processor`)
    Output mentah dari `/generator` (atau data dari `/sniffer`) diteruskan ke modul-modul di **`/processor`**. Di sinilah data **dianalisis, difilter, ditransformasi, atau dibersihkan** sesuai dengan logika yang ditentukan oleh `conf.json`.

6.  ### Penyimpanan Output (`/content`)
    Setelah data diolah oleh `/processor`, hasilnya akan **disimpan** ke direktori **`/content`**. `conf.json` dapat digunakan untuk menentukan format dan lokasi penyimpanan.

7.  ### Eksekusi Lanjutan (`/runner`)
    Jika tujuan bot melibatkan tindakan lebih lanjut berdasarkan data yang baru disimpan, modul di **`/runner`** akan diaktifkan. Ini bisa berarti **menjalankan skrip tambahan** atau memicu notifikasi, dengan jadwal atau pemicu yang diatur di `conf.json`.

8.  ### Pencatatan (`/log`)
    Sepanjang seluruh alur kerja ini, semua aktivitas penting, *error*, peringatan, dan status operasional akan secara otomatis **dicatat** ke dalam file log di direktori **`/log`**. Tingkat detail *logging* juga dapat dikonfigurasi di `conf.json`.

---

## Instalasi (Contoh)

Untuk menjalankan OtoBot, Anda mungkin perlu menginstal dependensi Python dan mengonfigurasi lingkungannya.

1.  **Kloning Repositori:**
    ```bash
    git clone [https://github.com/cloxt01/otoBots.git](https://github.com/cloxt01/otoBots.git)
    cd otoBots
    ```
2.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt # Asumsikan ada file requirements.txt
    ```
    *Jika tidak ada `requirements.txt`, Anda perlu menginstal setiap pustaka secara manual:*
    ```bash
    pip install [nama-pustaka-1] [nama-pustaka-2] ...
    ```

---

## Konfigurasi

Semua konfigurasi utama untuk OtoBot diatur dalam file **`conf/conf.json`**. Pastikan untuk mengedit file ini sesuai dengan tujuan dan parameter operasi yang Anda inginkan.

**Contoh `conf/conf.json`:**
```json
{
  "goals" : "Kumpulkan informasi harga pasar dari produk X di e-commerce X",
  "url": "https://example.store",

  "api" : {
    "domain": "api.xxx.com"
  },
  "browser": {
    "headlessMode": false,
    "profilePath": "C:\\Users\\(xxx)\\xxx.user"
  },
  "cookie": "head:value;xxx",
  "path" : {
    "content" : "content/",
    "runner" : "runner/",
    "log": "log/"
  },
  "ai": {
    "platform": "openrouter-ai",
    "maxTokens" : 16000,
    "apiKey": "sk-xxx"
  }
}
```
Sesuaikan nilai-nilai di atas sesuai dengan kebutuhan spesifik bot Anda.

## Penggunaan
Setelah instalasi dan konfigurasi, Anda dapat menjalankan OtoBot melalui main.py.

```json
python main.py
```

Bot akan mulai beroperasi sesuai dengan tujuan dan konfigurasi yang telah Anda tetapkan di conf/conf.json.
