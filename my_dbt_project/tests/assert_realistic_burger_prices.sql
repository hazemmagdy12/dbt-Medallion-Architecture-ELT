-- بنصطاد أي برجر متسجل في الاستيجنج بسعر خيالي (مثلاً أغلى من 2000)

SELECT 
    burger_id,
    burger_name,
    price
FROM {{ ref('stg_mongo_burgers') }}
WHERE price > 2000