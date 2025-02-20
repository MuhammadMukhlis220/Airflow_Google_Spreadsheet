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
