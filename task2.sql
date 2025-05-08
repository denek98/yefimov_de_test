WITH
  purchases AS (
    SELECT order_id, uploaded_at
    FROM `project.dataset.purchases`
  ),

  changed_ids AS (
    SELECT
      o.id AS order_id
    FROM `project.dataset.orders` AS o
    LEFT JOIN purchases AS p
      ON o.id = p.order_id
    WHERE p.order_id IS NULL
       OR o.updated_at > p.uploaded_at

    UNION ALL

    SELECT
      t.order_id
    FROM `project.dataset.transactions` AS t
    LEFT JOIN purchases AS p
      ON t.order_id = p.order_id
    WHERE t.updated_at > p.uploaded_at

    UNION ALL

    SELECT
      tx.order_id
    FROM `project.dataset.verification` AS v
    JOIN `project.dataset.transactions` AS tx
      ON v.transaction_id = tx.id
    LEFT JOIN purchases AS p
      ON tx.order_id = p.order_id
    WHERE v.updated_at > p.uploaded_at
  ),

  unique_ids AS (
    SELECT DISTINCT order_id
    FROM changed_ids
  )

SELECT
  o.*   EXCEPT(updated_at),
  t.*   EXCEPT(updated_at),
  v.*   EXCEPT(updated_at),
  CURRENT_TIMESTAMP() AS uploaded_at
FROM unique_ids AS u
JOIN `project.dataset.orders`       AS o  ON o.id = u.order_id
JOIN `project.dataset.transactions` AS t  ON t.order_id = u.order_id
JOIN `project.dataset.verification` AS v  ON v.transaction_id = t.id;
