
  
CREATE TABLE customers (
  customer_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  cpf_id VARCHAR(11) NOT NULL UNIQUE,
  gender CHAR(1) NOT NULL,
  birthdate DATE NOT NULL,
  phone_number VARCHAR(255),
  state VARCHAR(255),
  city VARCHAR(255),
  zipcode_prefix VARCHAR(5),
  created_at DATETIME NOT NULL
);
CREATE TABLE geolocation (
  geolocation_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  zipcode_prefix VARCHAR(5) NOT NULL UNIQUE,
  latitude DECIMAL(10,6) NOT NULL,
  longitude DECIMAL(10,6) NOT NULL,
  city VARCHAR(255) NOT NULL,
  state VARCHAR(255) NOT NULL
);
CREATE TABLE order_items (
  order_item_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  seller_id INT NOT NULL,
  quantity INT NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  freight_value DECIMAL(10,2) NOT NULL,
  discount DECIMAL(10,2) NOT NULL,
  net_price DECIMAL(10,2) NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id),
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
CREATE TABLE order_payments (
  order_payment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  payment_method VARCHAR(255) NOT NULL,
  payment_value DECIMAL(10,2) NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
CREATE TABLE order_reviews (
  order_review_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_id INT NOT NULL,
  review_id INT NOT NULL,
  review_rating INT NOT NULL,
  review_comment TEXT,
  created_at DATETIME NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (review_id) REFERENCES reviews(review_id)
);
CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  order_status VARCHAR(255) NOT NULL,
  order_date DATETIME NOT NULL,
  delivery_date DATETIME,
  ship_mode VARCHAR(255) NOT NULL,
  seller_id INT NOT NULL,
  freight_value DECIMAL(10,2) NOT NULL,
  net_total DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);
CREATE TABLE products (
  product_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  product_name VARCHAR(255) NOT NULL,
  product_description TEXT,
  product_category_name VARCHAR(255) NOT NULL,
  product_category_id INT NOT NULL,
  seller_id INT NOT NULL,
  manufacture_country VARCHAR(255),
  brand VARCHAR(255),
  price DECIMAL(10,2) NOT NULL,
  freight_value DECIMAL(10,2) NOT NULL,
  FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
);

