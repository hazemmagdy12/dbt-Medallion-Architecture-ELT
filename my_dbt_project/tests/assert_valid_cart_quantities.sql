-- بنصطاد الكميات الغريبة في السلال

SELECT 
    cart_item_id,
    user_id,
    quantity
FROM {{ ref('stg_redis_carts') }}
WHERE quantity <= 0 
   OR quantity > 100 -- بنفترض إن أقصى رقم منطقي ليوزر عادي هو 100