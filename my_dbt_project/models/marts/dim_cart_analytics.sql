{{
    config(
        materialized='table'
    )
}}

-- بنسحب الكوبري اللي جهزناه في الانترميديات
WITH cart_valuations AS (
    SELECT * FROM {{ ref('int_carts_with_prices') }}
)

-- تجميع الجدول النهائي وتسمية العواميد بأسماء بزنس واضحة جداً
SELECT 
    cart_item_id,
    user_id,
    burger_name,
    quantity,
    unit_price,
    total_item_price AS potential_revenue, -- سميناها إيرادات محتملة عشان بتاع المبيعات يفهمها
    is_available,
    cart_synced_at
    
FROM cart_valuations