import os
from munch import Munch
from airflow.models import Variable


airflow_env = os.getenv("AIRFLOW_ENV", "local")
config = {}

# local / sandbox
if airflow_env in ("local"):
    config.update({
        # airflow params
        "schedule": None,
        "start_date": None,
        "end_date": None,
        "catchup": False,
        "max_active_runs": 1,

        # adzuna api params
        "adzuna_app_id": Variable.get("ADZUNA_APP_ID"),
        "adzuna_app_key": Variable.get("ADZUNA_APP_KEY"),

        # databricks params
        "databricks_conn_id": "databricks_default",
        "target_catalog": "adzuna",
        "target_schema": "prj",
        "adzuna_table_name": "jobs"
    })


# clean up local variables
del airflow_env

# export as munch
config = Munch(config)
