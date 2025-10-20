-- Drop tables if they exist
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

-- Create table: products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    product_desc TEXT NOT NULL,
    product_cost INTEGER NOT NULL,
    product_category VARCHAR(55) NOT NULL,
    product_name_image TEXT NOT NULL
);

-- Insert data into products
INSERT INTO products (product_id, product_name, product_desc, product_cost, product_category, product_name_image) VALUES
(2, 'omo', 'cleaning', 80, 'detergent', 'omo.jpg'),
(3, 'samsung galaxy A04', 'Smartphone', 17000, 'Smartphone', 'Samsung Galaxy A04.jpg'),
(4, 'samsung galaxy', 'Smartphone', 20000, 'Smartphone', 'Samsung galaxy s23.jpg'),
(5, 'techno phantom x2 pro', 'Smartphone', 20000, 'Smartphone', 'Tecno phantom x2 pro.jpg'),
(6, 'tecno spark 8c', 'Smartphone', 20000, 'Smartphone', 'Tecno spark 8c.jpg'),
(7, 'Tecno spark 9pro', 'Smartphone', 21000, 'Smartphone', 'Tecno spark 9pro.jpg'),
(8, 'ariel', 'one time cleanliness', 50, 'detergent', 'ariel.webp'),
(9, 'bag1', 'good for books', 1500, 'BAGS', 'bag1.jpg'),
(10, 'bag3', 'stylish bag for travelling', 1500, 'BAGS', 'bag3.jpeg'),
(14, 'camon 19', 'Smartphone', 35000, 'Smartphone', 'camon 19.jpg'),
(15, 'clothe1', 'clothes of high fashion', 1, 'Clothes', 'clothe1.jpg'),
(16, 'clothe2', 'shirts for men', 2, 'Clothes', 'clothe2.jpg'),
(17, 'clothe3', 'stylish shirts', 1500, 'Clothes', 'clothe3.jpg'),
(18, 'clothe4', 'flannel shirt', 1500, 'Clothes', 'clothe4.jpg'),
(19, 'clothe5', 'stripped shirt', 1500, 'Clothes', 'clothe5.jpg'),
(20, 'clothe6', 'official shirt', 1500, 'Clothes', 'clothe6.jpg'),
(54, 'infinix hot4', 'Smartphone', 2000, 'Smartphone', 'infinix hot4.jpg'),
(66, 'redmi 9A', 'Smartphone', 35000, 'Smartphone', 'redmi 9A.jpg'),
(67, 'samsung1.jpeg', 'Smartphone', 56000, 'Smartphone', 'samsung1.jpeg'),
(68, 'samsung2', 'Smartphone', 130000, 'Smartphone', 'samsung2.jpg'),
(69, 'samsung3', 'Smartphone', 130000, 'Smartphone', 'samsung3.png'),
(70, 'samsung4', 'Smartphone', 130000, 'Smartphone', 'samsung4.jpg'),
(71, 'samsung5', 'Smartphone', 130000, 'Smartphone', 'samsung5.png'),
(72, 'samsung7', 'Smartphone', 130000, 'Smartphone', 'samsung7.jpg'),
(73, 'samsung8', 'Smartphone', 158000, 'Smartphone', 'samsung8.jpg'),
(74, 'samsung A13', 'Smartphone', 160000, 'Smartphone', 'samsung A13.jpg'),
(78, 'techno pop5 go', 'Smartphone', 13000, 'Smartphone', 'techno pop5 go.jpg');

-- Create table: users
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone VARCHAR(50) NOT NULL
);

-- Insert data into users
INSERT INTO users (username, password, email, phone) VALUES
('abraham', '123456789', 'abrahammramba916@gmail.com', '0759972854');
