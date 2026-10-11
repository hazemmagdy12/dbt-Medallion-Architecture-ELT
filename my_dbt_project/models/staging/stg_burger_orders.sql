{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

WITH source AS (
    -- 1. سحب البيانات الخام
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_burger_orders_key_value') }}
),

extracted_json AS (
    -- 2. فرد الـ JSON لنصوص عادية (بدون تنظيف)
    SELECT 
        order_data->>'_id' AS order_id,
        order_data->>'burger_id' AS burger_id,
        order_data->>'name' AS burger_name,
        order_data->'customer_info'->>'name' AS customer_name,
        order_data->'customer_info'->>'city' AS customer_city,
        order_data->>'price' AS price_raw,
        order_data->>'is_spicy' AS is_spicy_raw,
        order_data->>'order_date' AS order_date_raw,
        synced_at
    FROM source
),

cleaned_data AS (
    -- 3. التنظيف وتغيير أنواع البيانات
    SELECT 
        -- الـ IDs نظيفة زي ما هي
        order_id,
        burger_id,
        
        -- تأمين النصوص بـ TRIM احتياطياً
        TRIM(burger_name) AS burger_name,
        TRIM(customer_name) AS customer_name,
        TRIM(customer_city) AS customer_city,
        
        -- تحويل السعر لـ NUMERIC مع حمايته من المسافات الفاضية
        CAST(NULLIF(price_raw, '') AS NUMERIC) AS price,
        
        -- لو القيمة فاضية حولها لـ False، غير كده حولها لـ Boolean
        CASE 
            WHEN is_spicy_raw IS NULL OR is_spicy_raw = '' THEN false
            ELSE CAST(is_spicy_raw AS BOOLEAN)
        END AS is_spicy,
        
        -- موجه المرور للتواريخ (أمريكي أو عالمي ISO)
        CASE 
            WHEN order_date_raw LIKE '%T%' OR order_date_raw LIKE '%-%' 
                 THEN CAST(order_date_raw AS TIMESTAMP)::DATE
            WHEN order_date_raw LIKE '%/%' 
                 THEN TO_DATE(order_date_raw, 'MM/DD/YYYY')
            ELSE NULL 
        END AS order_date,
        
        -- عمود التتبع اللي طلبته لمعرفة مصدر الداتا
        'raw_burger_orders_key_value' AS source_table,
        
        -- عمود المزامنة المطلوب للـ Incremental
        synced_at
        
    FROM extracted_json
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  -- فلترة الريكوردات الجديدة بس
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}