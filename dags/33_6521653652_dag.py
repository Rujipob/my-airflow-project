from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# ฟังก์ชันสำหรับดึงข้อมูล
# ข้อมูลจาก: ข้อมูลรายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2568
# Dataset URL: https://data.go.th/dataset/zoo-visitors2568
# องค์กร: องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์
def extract_data(**kwargs):
    url = "https://opend.data.go.th/get-ckan/datastore_search"  # CKAN API endpoint
    params = {
        'resource_id': '15a9e41b-2f07-4b05-8e53-cb4119f24c7d',  # Resource ID: Zoo Visitors 2568 (สิงหาคม)
        'limit': 1000  # ดึงข้อมูลสูงสุด 1000 records
    }
    headers = {
        'api-key': 'iFWOIOiQvAKwxrdzQtHEctOZyQvuoSgw'  # API key สำหรับ Thailand Open Data
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    print(f"API Response - Success: {data.get('success')}, Total records: {data.get('result', {}).get('total', 0)}")
    kwargs['ti'].xcom_push(key='crypto_data', value=data)

# ฟังก์ชันสำหรับแปลงข้อมูล
def transform_data(**kwargs):
    data = kwargs['ti'].xcom_pull(key='crypto_data', task_ids='extract')
    # แปลงข้อมูลจาก CKAN API response
    records = data.get('result', {}).get('records', [])
    print(f"Transform - Retrieved {len(records)} records from extract task")
    df = pd.DataFrame(records)
    print(f"DataFrame shape: {df.shape}")
    
    # บันทึกข้อมูลเป็น CSV ด้วย UTF-8 encoding with BOM
    csv_path = '/opt/airflow/data/ckan_data.csv'
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} records to {csv_path} (CSV format)")
    kwargs['ti'].xcom_push(key='transformed_data_path', value=csv_path)

# ฟังก์ชันสำหรับโหลดข้อมูลเข้าฐานข้อมูล PostgreSQL
def load_to_db(db_host, db_name, db_user, db_pswd, db_port, data_path):
    df = pd.read_csv(data_path, encoding='utf-8-sig')
    current_timestamp = datetime.now()
    df['data_ingested_at'] = current_timestamp

    engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_pswd}@{db_host}:{db_port}/{db_name}")
    df.to_sql('ckan_visitors', con=engine, if_exists='replace', index=False)
    print(f"Success: Loaded {len(df)} records to {db_name}.ckan_visitors table.")

# กำหนด default_args
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 23),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# กำหนด DAG
dag = DAG(
    'ckan_data_etl',
    default_args=default_args,
    description='ETL Pipeline: ข้อมูลสถิติผู้เข้าชมสวนสัตว์ 2568 (Zoo Visitors 2568) | Source: https://data.go.th/dataset/zoo-visitors2568',
    schedule_interval=timedelta(days=1),
)

# สร้าง Task
extract = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    provide_context=True,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    provide_context=True,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load_to_db,
    op_kwargs={
        'db_host': 'recalls_db',
        'db_name': 'recalls_db',
        'db_user': 'admin',
        'db_pswd': 'admin',
        'db_port': 5432,
        'data_path': '/opt/airflow/data/ckan_data.csv'
    },
    dag=dag,
)

# กำหนดลำดับของ Task
extract >> transform >> load
