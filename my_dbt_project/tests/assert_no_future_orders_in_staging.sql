-- بنصطاد الأوردرات اللي جاية من تطبيق البرجر بتاريخ لسه مجاش

SELECT 
    order_id,
    order_date
FROM {{ ref('stg_burger_orders') }}
WHERE order_date > CURRENT_TIMESTAMP