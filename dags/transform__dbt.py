from datetime import datetime

from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import (
    KubernetesPodOperator,
)

DBT_PROJECT = "dbt-test"

ARTIFACT_REGION = "asia-southeast1-docker.pkg.dev"
PROJECT_ID = "joon-sandbox"
REPO_ID = "airflow-dev-container"
IMAGE = f"{ARTIFACT_REGION}/{PROJECT_ID}/{REPO_ID}/{DBT_PROJECT}"

default_args = {
    "owner": "nguyendnb",
    "retries": 0,
    "name": f"{DBT_PROJECT}-pod",
    "image": IMAGE,
    "image_pull_policy": "Always",
    "namespace": "composer-user-workloads",
    "config_file": "/home/airflow/composer_kube_config",
    "startup_timeout_seconds": 300
}

with DAG(
    dag_id="transform__dbt",
    start_date=datetime(2022, 8, 8),
    description=f"Invoke dbt run for `{DBT_PROJECT}`",
    catchup=False,
    schedule_interval=None,
    default_args=default_args,
    tags=["transform"],
) as dag:

    dbt_seed = KubernetesPodOperator(
        task_id="dbt_seed",
        cmds=[
            "dbt",
            "seed",
            "--profiles-dir",
            ".",
            "--project-dir",
            ".",
        ],
    )

    dbt_run = KubernetesPodOperator(
        task_id="dbt_run",
        cmds=[
            "dbt",
            "run",
            "--profiles-dir",
            ".",
            "--project-dir",
            ".",
        ],
    )

    dbt_test = KubernetesPodOperator(
        task_id="dbt_test",
        cmds=[
            "dbt",
            "test",
            "--profiles-dir",
            ".",
            "--project-dir",
            ".",
        ],
    )

    dbt_seed >> dbt_run >> dbt_test
