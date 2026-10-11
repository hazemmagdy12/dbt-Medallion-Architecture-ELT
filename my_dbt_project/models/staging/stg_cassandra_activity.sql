{{
    config(
        materialized='incremental',
        unique_key='id'
    )
}}

WITH source AS (
    -- 1. سحب البيانات الخام من الاسكيما البرونز
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_cassandra_activity') }}
),

extracted_json AS (
    -- 2. فرد الـ JSON لنصوص وتجهيزها للتنظيف
    SELECT 
        id,
        activity_data->>'action' AS action_type,
        activity_data->>'user_id' AS user_id,
        activity_data->>'burger_id' AS burger_id_raw,
        activity_data->>'activity_time' AS activity_time_raw,
        synced_at
    FROM source
),

cleaned_data AS (
    -- 3. التنظيف وتغيير أنواع البيانات
    SELECT 
        id,
        
        -- تنظيف الأكشنز (هنسيب الإيرور زي ما هو لقيمته التحليلية للـ Business)
        TRIM(action_type) AS action_type,
        
        -- تنظيف الـ User ID
        TRIM(user_id) AS user_id,
        
        -- تحويل الـ N/A في الـ burger_id إلى NULL حقيقي
        NULLIF(TRIM(burger_id_raw), 'N/A') AS burger_id,
        
        -- تحويل تاريخ النشاط إلى TIMESTAMP صريح
        CAST(activity_time_raw AS TIMESTAMP) AS activity_time,
        
        -- عمود التتبع اللي طلبته لمعرفة مصدر الداتا (Source Type)
        'raw_cassandra_activity' AS source_table,
        
        -- عمود المزامنة للـ Incremental load
        synced_at
        
    FROM extracted_json
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  -- فلترة السطور الجديدة بس بناءً على وقت المزامنة
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}