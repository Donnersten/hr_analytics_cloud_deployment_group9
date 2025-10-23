with src_employer as (select * from {{ ref('src_employer') }})


select
    {{ dbt_utils.generate_surrogate_key(['employer__workplace', 'workplace_address__municipality']) }} AS employer_id,
    workplace_address__municipality,
    EMPLOYER__WORKPLACE,
    MAX(EMPLOYER__NAME) AS EMPLOYER__NAME,
    MAX(EMPLOYER__ORGANIZATION_NUMBER) AS EMPLOYER__ORGANIZATION_NUMBER,
    MAX(WORKPLACE_STREET_ADRESS) AS WORKPLACE_STREET_ADRESS,
    MAX(WORKPLACE_REGION) AS WORKPLACE_REGION,
    MAX(WORKPLACE_POSTCODE) AS WORKPLACE_POSTCODE,
    MAX(WORKPLACE_CITY) AS WORKPLACE_CITY,
    MAX(WORKPLACE_COUNTRY) AS WORKPLACE_COUNTRY
from src_employer
group by employer__workplace, workplace_address__municipality

