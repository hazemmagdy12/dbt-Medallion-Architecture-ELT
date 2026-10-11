-- 1. الكونفيج: بنعرف dbt إننا عايزين الجدول ده يكون View خفيف
{{
    config(
        materialized='view'
    )
}}

-- 2. سحب الجداول النظيفة باستخدام ref() بدل source()
WITH carts AS (
    SELECT * FROM {{ ref('stg_redis_carts') }}
),

burgers AS (
    SELECT * FROM {{ ref('stg_mongo_burgers') }}
),

-- 3. منطقة الدمج وتطبيق قواعد البزنس
joined_carts AS (
    SELECT 
        -- عواميد من جدول السلة (الفاكت)
        c.cart_item_id,
        c.user_id,
        c.item_id,
        c.quantity,
        
        -- عواميد من جدول المنيو (الديمينشن)
        b.burger_name,
        b.price AS unit_price,
        b.is_available,
        
        -- الحسبة الجديدة (البزنس لوجيك)
        (c.quantity * b.price) AS total_item_price,
        
        -- وقت التحديث
        c.synced_at AS cart_synced_at
        
    FROM carts c
    -- استخدمنا LEFT JOIN عشان لو في منتج في السلة اتشال من المنيو بالغلط، السلة متختفيش من التقرير
    LEFT JOIN burgers b
        ON c.item_id = b.burger_id
)

-- 4. عرض النتيجة النهائية للكوبري
SELECT * FROM joined_carts