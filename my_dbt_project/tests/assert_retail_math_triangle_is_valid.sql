-- التيست ده بيصطاد أي سطر الإجمالي بتاعه مش بيساوي (السعر × الكمية)
SELECT 
    transaction_id,
    price_per_unit,
    quantity,
    total_spent,
    (price_per_unit * quantity) AS calculated_total
FROM {{ ref('stg_retail_store_sales') }}
-- استخدمنا ROUND عشان نتفادى كسور القروش في المحاسبة
WHERE ROUND(total_spent, 2) != ROUND((price_per_unit * quantity), 2)