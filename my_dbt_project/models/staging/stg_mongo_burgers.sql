{{
    config(
        materialized='incremental',
        unique_key='burger_id'
    )
}}

WITH source AS (
    -- 1. سحب البيانات الخام من الاسكيما البرونز
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_mongo_burgers') }}
),

extracted_json AS (
    -- 2. فرد الـ JSON لنصوص (بدون عمود المكونات بناءً على تصميمك المعماري)
    SELECT 
        mongo_payload->>'_id' AS burger_id_raw,
        mongo_payload->>'name' AS burger_name_raw,
        mongo_payload->>'price' AS price_raw,
        mongo_payload->>'is_available' AS is_available_raw,
        synced_at
    FROM source
),

cleaned_data AS (
    -- 3. التنظيف وتغيير أنواع البيانات
    SELECT 
        -- تنظيف النصوص من أي مسافات
        TRIM(burger_id_raw) AS burger_id,
        TRIM(burger_name_raw) AS burger_name,
        
        -- تحويل السعر لـ NUMERIC مع حمايته من المسافات الفاضية
        CAST(NULLIF(TRIM(price_raw), '') AS NUMERIC) AS price,
        
        -- تحويل حالة التوافر لـ BOOLEAN
        CAST(NULLIF(TRIM(is_available_raw), '') AS BOOLEAN) AS is_available,
        
        -- عمود التتبع لمعرفة مصدر الداتا
        'raw_mongo_burgers' AS source_table,
        
        -- عمود المزامنة للـ Incremental load
        synced_at
        
    FROM extracted_json
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  -- فلترة السطور الجديدة بس بناءً على وقت المزامنة
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}