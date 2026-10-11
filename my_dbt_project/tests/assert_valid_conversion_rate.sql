-- بنصطاد أي برجر نسبة مبيعاته طلعت فيها خرافات رياضية

SELECT 
    burger_id,
    total_interactions,
    total_orders_completed,
    conversion_rate_percentage
FROM {{ ref('int_burger_conversion_funnel') }}
WHERE conversion_rate_percentage < 0 
   OR conversion_rate_percentage > 100