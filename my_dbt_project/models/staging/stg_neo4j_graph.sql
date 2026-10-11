{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

WITH source AS (
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_neo4j_graph') }}
),

extracted_data AS (
    -- سحبنا الـ IDs والأسماء بس ورمينا التاريخ الفاضي
    SELECT 
        id,
        graph_payload->>'item_id' AS item_id_raw,
        graph_payload->>'user_name' AS user_name_raw,
        synced_at
    FROM source
),

cleaned_data AS (
    SELECT 
        id,
        
        -- تنظيف النصوص
        TRIM(item_id_raw) AS item_id,
        TRIM(user_name_raw) AS user_name,
        
        -- عمود التتبع زي ما اتعودنا
        'raw_neo4j_graph' AS source_table,
        
        synced_at
        
    FROM extracted_data
    -- فلترة بسيطة عشان لو في سطر جاي فاضي تماماً
    WHERE item_id_raw IS NOT NULL OR user_name_raw IS NOT NULL
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}