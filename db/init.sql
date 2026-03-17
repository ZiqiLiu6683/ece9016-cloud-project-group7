CREATE DATABASE IF NOT EXISTS products_db;
USE products_db;

CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    description VARCHAR(255)
);

INSERT INTO products (id, name, description) VALUES
(1, 'Apple', 'Red fruit'),
(2, 'Banana', 'Yellow fruit'),
(3, 'Orange', 'Citrus fruit')
ON DUPLICATE KEY UPDATE
name = VALUES(name),
description = VALUES(description);