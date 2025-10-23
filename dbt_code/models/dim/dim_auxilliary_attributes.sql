with src_auxilliary_attributes as (select * from {{ ref('src_auxilliary_attributes') }})

select
    {{ dbt_utils.generate_surrogate_key(['id']) }} as auxilliary_attributes_id,
    id,
    MAX(experience_required) as experience_required,
    MAX(access_to_own_car) as access_to_own_car,
    MAX(driving_license_required) as driving_license_required
from src_auxilliary_attributes
group by id