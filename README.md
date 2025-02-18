---
# **Integrating Fill Google Spreadsheet Automatic using Google's API with Airflow**

Di repository ini kita akan membahas bagaimana mengintegrasikan Apache Airflow dengan Google Spreadsheet. Di sini kita akan menemukan contoh skrip DAG (Directed Acyclic Graph) yang dapat digunakan untuk melakukan perintah **write** langsung ke worksheet milik Google Spreadsheet.

# Step 1 Konfigurasi Google Console

Akses url https://console.cloud.google.com/ dengan login akun gmail kemudian pilih `Select Project`.

![Alt Text](/pic/google_console_1.png)
Gambar 1

Isi `Project Name` dan `Project ID`. `Project ID` akan diisi otomatis oleh sistem.

![Alt Text](/pic/google_console_2.png)

Gambar 2

Di menu sebelah kiri pilih `APIs & Services` dan pilih `Library`

![Alt Text](/pic/google_console_3.png)

Gambar 3

Cari dan pilih Google Spreadsheet API

![Alt Text](/pic/google_console_4.png)

Gambar 4

Klik `ENABLE`

![Alt Text](/pic/google_console_5.png)

Gambar 5

Create Credential dengan memilih API milik `Google Sheets API` dan pilih tipe `Application data`

![Alt Text](/pic/google_console_6.png)

Gambar 6

Pada bagian `Service account details`, isi seluruh form yang kosong kemudian CREATE AND CONTINUE

![Alt Text](/pic/google_console_7.png)

Gambar 7
