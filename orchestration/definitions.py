from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
import os

import sys
sys.path.insert(0, "../data_extract_load")


from job_pipeline import jobads_source

# data warehouse directory
db_path = os.getenv("DUCKDB_PATH")

dlt_resource = DagsterDltResource()

@dlt_assets(
    dlt_source=jobads_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="jobsearch",
        destination=dlt.destinations.duckdb(db_path), #update destination
        dataset_name="staging",
    )
)
def dlt_load(context: dg.AssetExecutionContext, dlt:DagsterDltResource):
    yield from dlt.run(context=context)

dbt_project_directory = Path(__file__).parents[1] / "dbt_code"

profiles_dir = os.getenv("DBT_PROFILES_DIR")

dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)

# CLI commands
dbt_resource = DbtCliResource(project_dir=dbt_project)

# -> manifest in runtime
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


#jobs
job_dlt = dg.define_asset_job("job_dlt", selection=dg.AssetSelection.keys("dlt_jobads_source_jobsearch_resource_all"))

job_dbt = dg.define_asset_job("job_dbt", selection=dg.AssetSelection.key_prefixes("warehouse", "marts"))

schedule_dlt = dg.ScheduleDefinition(
    job = job_dlt,
    cron_schedule="15 13 * * *"
)

@dg.asset_sensor(asset_key=dg.AssetKey("dlt_jobads_source_jobsearch_resource_all"), job_name="job_dbt")

def dlt_load_sensor():
    yield dg.RunRequest()


# definitions

defs = dg.Definitions(
    assets = [dlt_load, dbt_models],
    resources= {"dlt": dlt_resource,
                "dbt": dbt_resource},
    jobs = [job_dlt, job_dbt],
    schedules= [schedule_dlt],
    sensors = {dlt_load_sensor},
)