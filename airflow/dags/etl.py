from etl_config import config
from airflow.decorators import task
from airflow.models import DAG, Variable
from scripts.adzuna import fetch_adzuna_to_spark_df, merge_to_delta_table, get_spark
import logging


with DAG(
    "adzuna_etl_dag",
    max_active_runs = config.max_active_runs,
    schedule = config.schedule,
    start_date = config.start_date,
    end_date = config.end_date,
    catchup = config.catchup,
    tags = ["adzuna"]
) as dag:

    @task
    def load_adzuna_jobs():
        spark = get_spark()
        df = fetch_adzuna_to_spark_df(
            spark, 
            adzuna_app_id=Variable.get("ADZUNA_APP_ID"),
            adzuna_app_key=Variable.get("ADZUNA_APP_KEY"),
            max_days_old=3
        )
        logging.info(f"number of fetched records from Adzuna = {df.count()}")

        logging.info("Merging fetched data into databricks delta table")
        merge_to_delta_table(spark, df)
        
        table_records_cnt = spark.sql(f"select count(*) from adzuna.prj.jobs").collect()[0][0]
        logging.info(f"Number of records after merge: {table_records_cnt}")

        logging.info("Closing spark session")
        if spark:
            spark.stop()
        
        logging.info("Done")

    load_task = load_adzuna_jobs()
