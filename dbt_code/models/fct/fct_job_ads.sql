with job_ads as (

    select * from {{ ref('src_job_ads') }}

)
 
select

    {{ dbt_utils.generate_surrogate_key(['occupation__label']) }} as occupation_id,

    {{ dbt_utils.generate_surrogate_key(['id']) }} AS job_details_id,

    {{ dbt_utils.generate_surrogate_key(['employer__workplace', 'workplace_address__municipality']) }} AS employer_id,

    {{ dbt_utils.generate_surrogate_key(['id']) }} as auxilliary_attributes_id,

    cast(vacancies as integer) as vacancies,   -- 👈 fix

    relevance,

    application_deadline

from job_ads

 