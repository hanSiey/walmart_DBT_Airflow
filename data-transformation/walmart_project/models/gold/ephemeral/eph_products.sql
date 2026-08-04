SELECT DISTINCT
    product_id,
    product_name,
    category,
    brand,
    price,
    product_created_timestamp,
    product_updated_timestamp,
    current_timestamp() AS gold_processed_at
FROM 
    {{ref('obt_b')}}