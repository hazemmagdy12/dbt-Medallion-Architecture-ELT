-- التست ده بيتأكد إن لو العدد أكبر من صفر، لازم اللستة متبقاش فاضية
SELECT 
    burger_id
FROM {{ ref('int_menu_with_ingredients') }}
WHERE (ingredients_count > 0 AND ingredients_list IS NULL)
   OR (ingredients_count = 0 AND ingredients_list IS NOT NULL)