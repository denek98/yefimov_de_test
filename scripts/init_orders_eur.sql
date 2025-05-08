CREATE TABLE IF NOT EXISTS orders_eur (
    order_id UUID PRIMARY KEY,
    customer_email TEXT NOT NULL,
    order_date TIMESTAMP NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    currency TEXT NOT NULL
);