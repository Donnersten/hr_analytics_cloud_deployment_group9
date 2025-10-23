with stg_job_ads as (select * from {{ source('hr_project_db', 'stg_ads') }})

select
    occupation_group__concept_id as occupation_group__concept_id,
    occupation_field__concept_id as occupation_group__field_id,
    occupation__label as occupation,
    occupation_group__label as occupation_group,
    occupation_field__label as occupation_field
from stg_job_ads