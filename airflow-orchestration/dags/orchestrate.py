from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import RunLifeCycleState, RunResultState
from dotenv import load_dotenv
import time, os

load_dotenv()

@dag
def orchestrate():
    #DATABRICKS TASK
    @task
    def ingest_cdc():
        ws = WorkspaceClient(
            host=os.getenv("DB_HOST"),
            token=os.getenv("API_TOKEN"),
        )

        job_trigger = ws.jobs.run_now(job_id=737253478558767)

        while True:
            job_run = ws.jobs.get_run(run_id=job_trigger.run_id)

            if job_run.state.life_cycle_state in [RunLifeCycleState.TERMINATED, RunLifeCycleState.SKIPPED, RunLifeCycleState.INTERNAL_ERROR]:
                if job_run.state.result_state == RunResultState.SUCCESS:
                    print("Job completed successfully.")
                    break
                else:
                    raise Exception(f"Job failed with state: {job_run.state.result_state}")

            time.sleep(5)  # Wait for 10 seconds before checking the job status again
        return "CDC data ingested"

    @task.bash
    def clean_target():
        return "rm -rf /opt/airflow/walmart_project/target && rm -rf /opt/airflow/walmart_project/dbt_packages && rm -rf /opt/airflow/walmart_project/logs"

    #DBT TASKS
    @task.bash
    def source_freshness():
        #Manually set the working directory to the dbt project directory
        return "cd /opt/airflow/walmart_project && dbt source freshness"

    silver_technical = BashOperator(
        task_id='silver_technical',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select silver'
    )

    silver_technical_test = BashOperator(
        task_id='silver_technical_test',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt test --select silver'
    )

    silver_business = BashOperator(
        task_id='silver_business',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select silver_b'
    )

    gold_ephermeral = BashOperator(
        task_id='gold_ephermeral',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select gold/ephemeral'
    )

    gold_dimensions = BashOperator(
        task_id='gold_dimensions',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt snapshot'
    )

    gold_facts = BashOperator(
        task_id='gold_facts',
        cwd='/opt/airflow/walmart_project',
        bash_command='dbt run --select gold/facts'
    )

    ingest_cdc() >> clean_target() >> source_freshness() >> silver_technical >> silver_technical_test >> silver_business >> gold_ephermeral >> gold_dimensions >> gold_facts

orchestrate_dag = orchestrate()