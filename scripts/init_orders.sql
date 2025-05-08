CREATE TABLE IF NOT EXISTS orders (
    order_id UUID PRIMARY KEY,
    customer_email TEXT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);

