# Airflow ETL Project

## About project

This project showcases an ETL pipeline built using Apache Airflow to retrieve job listing data from the Adzuna API, transform it, and load it into a Databricks delta table. The entire setup runs in Docker, ensuring a consistent and reproducible environment for extracting, transforming, and loading data.

For more details, check <link to article>

## Prerequisites

To run this project, you need the following:
 - Adzuna API account at `https://developer.adzuna.com/` with `Application ID` and `Application Key`
 - Databricks Free Edition account `https://www.databricks.com/learn/free-edition`
 - Docker and VS Code installed


## How to Run the Pipeline

1. Clone the project github repo
```
git clone https://github.com/kazarmax/airflow_databricks_etl.git
```

2. Open the project folder in VS Code

3. Run Airflow services in docker

```
docker compose up -d
```

4. Open Airflow UI at `http://localhost:8080/` (login/password: airflow/airflow)

5. In Airflow UI, add and fill in variables `ADZUNA_APP_ID` and `ADZUNA_APP_KEY` using values from your Adzuna API account

6. In Airflow UI, add a Connection to Databricks. Fill in the Host and Password fields using your databricks account. For the password, generate and use personal token from Databricks.

7. Create catalog, schema and table in databricks unity catalog by running the following command in the terminal locally:

```
docker compose exec -T airflow-scheduler python /opt/python/scripts/databricks_ddl.py
```

8. In Airflow UI, open and run the `load_adzuna_jobs` DAG

9. Upon successful execution of the DAG, log in to Databricks and check if the table `adzuna.prj.jobs` exists and contains data.
