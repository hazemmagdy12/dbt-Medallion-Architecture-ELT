-- التست ده بيصطاد السلال اللي سعرها باظ لأن الساندوتش اتحذف من المنيو
SELECT 
    cart_item_id
FROM {{ ref('int_carts_with_prices') }}
WHERE total_item_price IS NULL 
   OR total_item_price < 0