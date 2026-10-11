{{
    config(
        materialized='incremental',
        unique_key='transaction_id'
    )
}}

WITH source AS (
    SELECT * 
    FROM {{ source('bronze_csv', 'retail_store_sales') }}
),

staged AS (
    -- تطبيق قواعد التنظيف والـ Business Logic
    SELECT 
        -- 1. Primary Keys & IDs
        TRIM(transaction_id)::VARCHAR AS transaction_id,
        TRIM(customer_id)::VARCHAR AS customer_id,
        COALESCE(TRIM(item), 'Unknown_Item')::VARCHAR AS item_code,

        -- 2. Categorical Data Standardization
        CASE 
            WHEN TRIM(category) = 'Computers and electric accessories' THEN 'Computers'
            WHEN TRIM(category) = 'Electric household essentials' THEN 'Appliances'
            WHEN TRIM(category) = 'Milk Products' THEN 'Dairy'
            WHEN TRIM(category) = 'Patisserie' THEN 'Bakery'
            WHEN TRIM(category) = 'Butchers' THEN 'Meat'
            ELSE TRIM(category) 
        END AS category_name,
        
        COALESCE(TRIM(payment_method), 'Unknown')::VARCHAR AS payment_method,
        COALESCE(TRIM(location), 'Unknown')::VARCHAR AS location,

        -- 3. Financials (The Math Triangle)
        COALESCE(price_per_unit, (total_spent / NULLIF(quantity, 0)))::DECIMAL(10,2) AS price_per_unit,
        COALESCE(quantity, (total_spent / NULLIF(price_per_unit, 0)))::INT AS quantity,
        COALESCE(total_spent, (price_per_unit * quantity))::DECIMAL(10,2) AS total_spent,

        -- 4. Dates & Booleans
        CAST(transaction_date AS DATE) AS transaction_date,
        COALESCE(discount_applied::BOOLEAN, FALSE) AS has_discount, 
        _fivetran_synced
        
    FROM source
)

SELECT * FROM staged

{% if is_incremental() %}
  WHERE _fivetran_synced > (SELECT MAX(_fivetran_synced) FROM {{ this }})
{% endif %}