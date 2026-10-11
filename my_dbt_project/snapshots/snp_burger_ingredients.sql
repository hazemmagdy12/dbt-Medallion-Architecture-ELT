{% snapshot snp_burger_ingredients %}

{{
    config(
        target_schema='snapshots',      
        unique_key='burger_ingredient_id', 
        strategy='timestamp',           
        updated_at='synced_at'          
    )
}}

SELECT * FROM {{ ref('stg_burger_ingredients') }}

{% endsnapshot %}