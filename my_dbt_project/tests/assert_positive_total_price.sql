-- التست هينجح لو الكود ده مرجعش أي حاجة
-- إحنا هنا بنصطاد السطور اللي سعرها أقل من أو يساوي صفر

SELECT 
    cart_item_id,
    item_id,
    total_item_price
FROM {{ ref('int_carts_with_prices') }}
WHERE total_item_price <= 0