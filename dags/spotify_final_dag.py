import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine

import sys
sys.path.append('/opt/airflow/scripts')

# from airflow.utils.dates import days_ago
from scripts.spotify_etl import spotify_etl

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2023, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1)
}

dag = DAG(
    'spotify_final_dag',
    default_args=default_args,
    description='Spotify ETL process every 50 minutes',
    schedule_interval=dt.timedelta(minutes=50),
)

def run_etl(**kwargs):
    print("Stated Spotify ETL Task.....")
    conn = BaseHook.get_connection('postgre_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    spotify_etl(engine=engine) #pass engine into etl to use postgres
    print("ETL completed and data loaded successfully.")


create_my_played_tracks = PostgresOperator(
    task_id='create_my_played_tracks',
    postgres_conn_id='postgre_sql',
    sql="""
            CREATE TABLE IF NOT EXISTS my_played_tracks(
            song_name VARCHAR(200),
            artist_name VARCHAR(200),
            played_at VARCHAR(200),
            timestamp VARCHAR(200),
            PRIMARY KEY (played_at)
        );
        """,
        dag=dag
)

create_fav_artist = PostgresOperator(
    task_id='create_fav_artist',
    postgres_conn_id='postgre_sql',
    sql="""
        CREATE TABLE IF NOT EXISTS fav_artist(
            timestamp VARCHAR(200),
            ID VARCHAR(200),
            artist_name VARCHAR(200),
            count VARCHAR(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (ID)
        );
    """,
    dag=dag
)

run_etl_task = PythonOperator(
    task_id='run_spotify_etl',
    python_callable=run_etl,
    dag=dag,
)

[create_my_played_tracks, create_fav_artist] >> run_etl_task


