with stg_job_ads as (select * from {{ source('hr_project_db', 'stg_ads') }})

select 
    occupation__label,
    number_of_vacancies as vacancies,
    relevance,
    application_deadline,
    id,
    employer__workplace,
    workplace_address__municipality,
from stg_job_ads
order by application_deadline