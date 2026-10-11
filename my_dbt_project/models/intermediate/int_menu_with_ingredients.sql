{{
    config(
        materialized='view'
    )
}}

WITH burgers AS (
    SELECT * FROM {{ ref('stg_mongo_burgers') }}
),

ingredients AS (
    SELECT * FROM {{ ref('stg_burger_ingredients') }}
),

-- 1. الخطوة دي هي اللي بتحمينا من تكرار الداتا (تضبيط الـ Grain)
grouped_ingredients AS (
    SELECT 
        burger_id,
        -- الدالة دي بتلم السطور المتعددة وتحطهم في نص واحد بينهم فاصل
        STRING_AGG(ingredient_name, ', ') AS ingredients_list,
        -- وممكن كمان نعدهم بالمرة عشان لو البزنس عايز يعرف البرجر ده فيه كام مكون
        COUNT(ingredient_name) AS ingredients_count
    FROM ingredients
    GROUP BY burger_id
),

-- 2. الدمج النهائي بين المنيو والمكونات المتجمعة
joined_menu AS (
    SELECT 
        b.burger_id,
        b.burger_name,
        b.price,
        b.is_available,
        g.ingredients_list,
        g.ingredients_count
        
    FROM burgers b
    -- استخدمنا LEFT JOIN عشان لو برجر لسه متسجلوش مكونات ميختفيش من المنيو
    LEFT JOIN grouped_ingredients g
        ON b.burger_id = g.burger_id
)

SELECT * FROM joined_menu