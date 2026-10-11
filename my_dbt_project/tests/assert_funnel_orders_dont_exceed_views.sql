-- التست ده بيصطاد أي برجر مبيعاته تخطت مشاهداته (لأن ده معناه إن في مشكلة في تتبع المشاهدات)
SELECT 
    burger_id,
    burger_name
FROM {{ ref('int_burger_conversion_funnel') }}
WHERE total_orders_completed > total_interactions