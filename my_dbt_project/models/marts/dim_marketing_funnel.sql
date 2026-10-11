{{
    config(
        materialized='table'
    )
}}

-- بنسحب كوبري الـ Funnel اللي تعبنا فيه وعالجنا فيه الـ NULL وضبطنا فيه الـ Grain
WITH funnel_logic AS (
    SELECT * FROM {{ ref('int_burger_conversion_funnel') }}
)

SELECT 
    burger_id,
    burger_name,
    total_interactions AS total_views_and_clicks,
    total_orders_completed AS actual_purchases,
    conversion_rate_percentage,
    total_revenue
    
FROM funnel_logic
-- بنرتب الجدول أوتوماتيك من أعلى معدل تحويل لأقل معدل عشان نريح بتوع التسويق
ORDER BY conversion_rate_percentage DESC