---
# **Integrating Fill Google Spreadsheet Automatic using Google's API with Airflow**

Di repository ini kita akan membahas bagaimana mengintegrasikan Apache Airflow dengan Google Spreadsheet. Di sini kita akan menemukan contoh skrip DAG (Directed Acyclic Graph) yang dapat digunakan untuk melakukan perintah **write** langsung ke worksheet milik Google Spreadsheet.

## Step 1 Konfigurasi Google Cloud Console

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

Pada bagian `Service account details`, isi seluruh form yang kosong kemudian `CREATE AND CONTINUE`

![Alt Text](/pic/google_console_7.png)

Gambar 7

Pada bagian `Grant this service account access to project`, isi bagian `Role` dengan **Owner** kemudian `CONTINUE`

![Alt Text](/pic/google_console_8.png)

Gambar 8

Kembali ke menu sebelah kiri, pilih bagian `IAM and Admin` dan ke `Service Accounts`. DI bagian email, pilih akun yang baru saja kita buat.

![Alt Text](/pic/google_console_9.png)

Gambar 9

Di dalam akun yang dipilih, pergi ke tab `KEYS` dan pilih `Create new key` 

![Alt Text](/pic/google_console_10.png)

Gambar 10

Kemudian pilih `JSON` dan `CREATE`

![Alt Text](/pic/google_console_11.png)

Gambar 11

FIle JSON akan otomatis ter-download oleh browser

![Alt Text](/pic/google_console_12.png)

Gambar 12

Buat Spreadsheet baru (Di sini saya menamakannya dengan `Testing Spreadsheet API`) dan `Share` dokumen tersebut dengan mengisi email yang baru kita buat di Google Cloud Console serta beri role **Editor**

![Alt Text](/pic/google_console_13.png)

Gambar 13

Jika kesulitan menemukan email yang dibuat, buka file JSON yang diunduh tadi dan cek di bagian **client_email**

![Alt Text](/pic/code_1.png)

Gambar 14

# Step 2 Test Menggunakan Code Editor (Python)

Di sini saya menggunakan Jupyter Notebook pada VS Code.
Library yang dibutuhkan adalah gspread dan oauth2client.service_account

![Alt Text](/pic/code_3.png)

Gambar 15

Masukan variabel scope dengan `["https://www.googleapis.com/auth/spreadsheets"]`
Variabel creds dengan path ke file JSON yang diunduh

Pada bagian spreadsheet_id, kita bisa cek pada url dokumen spreadsheet yang dituju seperti pada gambar 16

![Alt Text](/pic/code_2.png)

Gambar 16

Dari code gambar 15, kita akan meminta nama (title) dari Spreadsheet yang kita tuju dan nama sheet-nya

Setelah berhasil, kita akan melanjutkan untuk memberi perintah write ke cell A5 dan A6 dengan dua metode.
Metode pertama dengan mengirim API satu per satu dan metode kedua dengan mengirim API menggunakan Batch.
API yang kita buat ini dilimit oleh Google sebanyak 30 kali penulisan dalah sehari sehingga akan lebih bijak dengan menggunakan metode Batch

Kotak merah yang atas adalah cara untuk mengirim API satu per satu. Kota merah yang bawah adalah cara mengirim API menggunakan Batch.

![Alt Text](/pic/code_4.png)

Gambar 17

Result:

![Alt Text](/pic/result_3.png)

Gambar 18

## Step 3 Buat DAG Airflow

Setelah berhasil testing menggunakan code editor, sekarang kita akan implementasikan ke Apache Airflow

For the complete Python programming code, refer to the following block.
<details>
   <summary>Click to view the complete Python code.</summary>

   ```python
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import gspread # pip install gspread
from oauth2client.service_account import ServiceAccountCredentials # pip install oauth2client

default_args = {
    'owner': 'mukhlis',
    'start_date': datetime(2025, 2, 12)
}

dag = DAG(
    'send_google_spreadsheet_api',
    default_args=default_args,
    catchup=False,
    schedule_interval=None,
    tags=['test', 'google spreadsheet', 'python']
)

def first_task():
    print("Our First Task")
    
def second_task():
    print("Our Second Task")
    
def send_result_google():
    scope = ["https://www.googleapis.com/auth/spreadsheets"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("/usr/odp/0.2.0.0-04/airflow/data/google_spreadsheet_api/circular-symbol-450703-v0-2328556ec71b.json", scope)
    client = gspread.authorize(creds)

    spreadsheet_id = '1n-siq_lmQ-_zXB7U4Dz4l643FaOZogLSuswj8Ic5paM'
    spreadsheet = client.open_by_key(spreadsheet_id)
    
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    
    message_text = f"All task Done at:"
    message_time = current_date
    
    sheet = spreadsheet.get_worksheet(0)
    sheet.update(range_name='A5', values=[[message_text]])
    sheet.update(range_name='B5', values=[[message_time]])
    
t1 = PythonOperator(
    task_id='first_task',
    python_callable=first_task,
    dag=dag
)

t2 = PythonOperator(
    task_id='second_task',
    python_callable=second_task,
    dag=dag
)

t3 = PythonOperator(
    task_id='send_automatic_fill_spreadsheet',
    python_callable=send_result_google,
    dag=dag
)

t1 >> t2 >> t3

   ```
   </details>


