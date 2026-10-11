{{
    config(
        materialized='incremental',
        unique_key='burger_ingredient_id'
    )
}}

WITH source AS (
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_mongo_burgers') }}
    -- التعديل الأول هنا: ضفنا حرف b للدالة
    WHERE mongo_payload->'ingredients' IS NOT NULL 
      AND jsonb_typeof(mongo_payload->'ingredients') = 'array'
),

exploded_ingredients AS (
    SELECT 
        mongo_payload->>'_id' AS burger_id_raw,
        ingredient.value AS ingredient_name_raw,
        synced_at
    FROM source
    -- التعديل التاني هنا: ضفنا حرف b لدالة التفجير
    CROSS JOIN jsonb_array_elements_text(mongo_payload->'ingredients') AS ingredient(value)
),

cleaned_data AS (
    SELECT 
        -- بناء Surrogate Key
        MD5(TRIM(burger_id_raw) || '-' || TRIM(ingredient_name_raw)) AS burger_ingredient_id,
        
        -- الـ Foreign Key
        TRIM(burger_id_raw) AS burger_id,
        
        -- تنظيف اسم المكون
        TRIM(ingredient_name_raw) AS ingredient_name,
        
        -- عمود التتبع
        'raw_mongo_burgers' AS source_table,
        
        -- عمود المزامنة للـ Incremental load
        synced_at
        
    FROM exploded_ingredients
    WHERE TRIM(ingredient_name_raw) != ''
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}