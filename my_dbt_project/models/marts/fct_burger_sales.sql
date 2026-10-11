-- 1. الكونفيج: هنا في تغيير جوهري! ركز فيه
{{
    config(
        materialized='table'
    )
}}

-- 2. سحب الداتا: هنسحب الفاكت (الأوردرات) والكوبري الجاهز بتاعنا (المنيو والمكونات)
WITH fact_orders AS (
    SELECT * FROM {{ ref('stg_burger_orders') }}
),

dim_menu AS (
    SELECT * FROM {{ ref('int_menu_with_ingredients') }}
),

-- 3. تجميع الـ One Big Table (OBT)
final_mart AS (
    SELECT 
        -- أرقام وحركات البزنس (من الفاكت)
        o.order_id,
        o.customer_name,
        o.price AS order_price,
        o.synced_at AS order_time,
        
        -- تفاصيل الوصف (من الديمينشن الجاهز)
        m.burger_name,
        m.is_available AS is_currently_available,
        m.ingredients_list,
        m.ingredients_count
        
    FROM fact_orders o
    -- بنلزق الديمينشن في الفاكت
    LEFT JOIN dim_menu m
        ON o.burger_id = m.burger_id
)

-- 4. العرض النهائي
SELECT * FROM final_mart