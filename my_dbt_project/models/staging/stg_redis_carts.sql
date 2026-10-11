{{
    config(
        materialized='incremental',
        unique_key='cart_item_id'
    )
}}

WITH source AS (
    -- سحبنا الداتا واستبعدنا أي سلة مفهاش منتجات
    SELECT * 
    FROM {{ source('bronze_burger_app', 'raw_redis_carts') }}
    WHERE cart_payload->'cart_items' IS NOT NULL
),

exploded_carts AS (
    -- هنا السحر بتاع تفكيك القاموس لسطور
    SELECT 
        cart_payload->>'user_id' AS user_id_raw,
        cart_item.key AS item_id_raw,
        cart_item.value AS quantity_raw,
        captured_at
    FROM source
    -- الدالة دي بتخلق جدول وهمي فيه عمودين (key للـ item_id، و value للكمية)
    CROSS JOIN jsonb_each_text(cart_payload->'cart_items') AS cart_item(key, value)
),

cleaned_data AS (
    SELECT 
        -- Surrogate Key (دمج اليوزر مع المنتج عشان نمنع التكرار)
        MD5(TRIM(user_id_raw) || '-' || TRIM(item_id_raw)) AS cart_item_id,
        
        -- تنظيف البيانات
        TRIM(user_id_raw) AS user_id,
        TRIM(item_id_raw) AS item_id,
        
        -- تحويل الكمية لرقم صحيح
        CAST(TRIM(quantity_raw) AS INTEGER) AS quantity,
        
        -- عمود التتبع
        'raw_redis_carts' AS source_table,
        
        -- توحيد اسم عمود الوقت عشان الـ dbt
        captured_at AS synced_at
        
    FROM exploded_carts
)

SELECT * FROM cleaned_data

{% if is_incremental() %}
  WHERE synced_at > (SELECT MAX(synced_at) FROM {{ this }})
{% endif %}