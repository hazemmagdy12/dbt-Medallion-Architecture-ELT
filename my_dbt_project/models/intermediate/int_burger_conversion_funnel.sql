{{
    config(
        materialized='view'
    )
}}

-- 1. نضغط جدول الأكتيفيتي (نعد التفاعلات لكل برجر)
WITH activity_summary AS (
    SELECT 
        burger_id,
        -- بنعد كم مرة البرجر ده ظهر أو الناس داست عليه
        COUNT(id) AS total_interactions
    FROM {{ ref('stg_cassandra_activity') }}
    GROUP BY burger_id
),

-- 2. نضغط جدول الأوردرات (نعد المبيعات لكل برجر)
sales_summary AS (
    SELECT 
        burger_id,
        COUNT(order_id) AS total_orders_completed,
        SUM(price) AS total_revenue
    FROM {{ ref('stg_burger_orders') }}
    GROUP BY burger_id
),

-- 3. نجيب المنيو كعمود فقري ونربط معاه التجميعات دي
funnel_logic AS (
    SELECT 
        b.burger_id,
        b.burger_name,
        
        -- استخدمنا COALESCE عشان لو برجر متشفش خالص نحط 0 بدل NULL
        COALESCE(a.total_interactions, 0) AS total_interactions,
        COALESCE(s.total_orders_completed, 0) AS total_orders_completed,
        COALESCE(s.total_revenue, 0) AS total_revenue,
        
        -- البزنس لوجيك الأعظم: حساب معدل التحويل (الطلبات ÷ المشاهدات)
        CASE 
            WHEN a.total_interactions > 0 
            THEN ROUND((s.total_orders_completed::NUMERIC / a.total_interactions) * 100, 2)
            ELSE 0 
        END AS conversion_rate_percentage
        
    FROM {{ ref('stg_mongo_burgers') }} b
    LEFT JOIN activity_summary a ON b.burger_id = a.burger_id
    LEFT JOIN sales_summary s ON b.burger_id = s.burger_id
)

SELECT * FROM funnel_logic