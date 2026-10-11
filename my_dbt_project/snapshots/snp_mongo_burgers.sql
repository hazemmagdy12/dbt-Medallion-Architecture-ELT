{% snapshot snp_mongo_burgers %}

{{
    config(
        target_schema='snapshots',
        unique_key='burger_id',
        
        strategy='check',
        
        check_cols=['price', 'is_available']
    )
}}
SELECT * FROM {{ ref('stg_mongo_burgers') }}

{% endsnapshot %}