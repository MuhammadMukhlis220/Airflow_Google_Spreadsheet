---
# **Integrating Fill Google Spreadsheet Automatic using Google's API with Airflow**

In this repository, we will learn how to integrate Apache Airflow with Google Spreadsheet. Here, we will find an example of a DAG (Directed Acyclic Graph) script that can be used to perform **write** commands directly to a Google Spreadsheet worksheet.

## Step 1 Configure Google Cloud Console

Access the URL [https://console.cloud.google.com/](https://console.cloud.google.com/) and log in with your Gmail account. Then, select `Select Project`.

![Alt Text](/pic/google_console_1.png)
Figure 1

Enter the `Project Name` and `Project ID`. The `Project ID` will be automatically filled by the system.

![Alt Text](/pic/google_console_2.png)

Figure 2

On the left menu, select `APIs & Services` and then choose `Library`.

![Alt Text](/pic/google_console_3.png)

Figure 3

Search for and select the Google Sheets API.

![Alt Text](/pic/google_console_4.png)

Figure 4

Click `ENABLE`

![Alt Text](/pic/google_console_5.png)

Figure 5

Click on `Create Credential`, select the API for `Google Sheets API`, and choose the type `Application data`.

![Alt Text](/pic/google_console_6.png)

Figure 6

In the `Service account details` section, fill out all the empty fields and then click `CREATE AND CONTINUE`.

![Alt Text](/pic/google_console_7.png)

Figure 7

In the `Grant this service account access to project` section, fill in the `Role` field with **Owner** and then click `CONTINUE`.

![Alt Text](/pic/google_console_8.png)

Figure 8

Return to the left-hand menu, select `IAM and Admin`, and then go to `Service Accounts`. In the email section, select the account that we just created.

![Alt Text](/pic/google_console_9.png)

Figure 9

In the selected account, go to the `KEYS` tab and select `Create new key`.

![Alt Text](/pic/google_console_10.png)

Figure 10

Then select `JSON` and then `CREATE`

![Alt Text](/pic/google_console_11.png)

Figure 11

The JSON file will be automatically downloaded by the browser.

![Alt Text](/pic/google_console_12.png)

Figure 12

Create a new Spreadsheet (I named it `Testing Spreadsheet API`) and `Share` the document by entering the email you just created in the Google Cloud Console, granting it the **Editor** role.

![Alt Text](/pic/google_console_13.png)

Figure 13

If you're having trouble finding the email that was created, open the JSON file that was downloaded earlier and check under the **client_email** section.

![Alt Text](/pic/code_1.png)

Figure 14

# Step 2: Testing Using a Code Editor (Python)

In this step, I am using Jupyter Notebook in VS Code. 
The required libraries are `gspread` and `oauth2client.service_account`.

![Alt Text](/pic/code_3.png)

Figure 15

Add the `scope` variable with the value `["https://www.googleapis.com/auth/spreadsheets"]`. 
Set the `creds` variable to the path of the downloaded JSON file.

In the `spreadsheet_id` section, we can check the URL of the target spreadsheet document as shown in Figure 16.

![Alt Text](/pic/code_2.png)

Figure 16

From the code in Figure 15, we will request the name (title) of the target Spreadsheet and its sheet name.

Once successful, we will proceed to send write commands to cells A5 and A6 using two methods. The first method involves sending individual API calls one by one, while the second method uses Batch API calls. This API we created is limited by Google to 30 write operations per day, so it would be wiser to use the Batch method.

The upper red box shows how to send API calls one by one, while the lower red box demonstrates how to send API calls using the Batch method.

![Alt Text](/pic/code_4.png)

Figure 17

Result:

![Alt Text](/pic/result_3.png)

Figure 18

## Step 3 Create Airflow DAG

After successfully testing using the code editor, we will now implement it in Apache Airflow.

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

In this section, we simulate time logging after all tasks have been completed in cells A5 and B5. We capture the current time using `datetime.now()` from the `datetime` library.

![Alt Text](/pic/result_1.png)

Figure 19

Let’s run the DAG.

![Alt Text](/pic/result_2.png)

Figure 20

## Step 4 Check the Results

The results from the executed DAG:

![Alt Text](/pic/code_5.png)

Figure 21

---
**This tutorial has been created, happy experimenting!**
