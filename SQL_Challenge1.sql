create database challenge1;
use challenge1;


CREATE TABLE sales (
  customer_id VARCHAR(1),
  order_date DATE,
  product_id INTEGER
);

INSERT INTO sales
  (customer_id, order_date, product_id)
VALUES
  ('A', '2021-01-01', '1'),
  ('A', '2021-01-01', '2'),
  ('A', '2021-01-07', '2'),
  ('A', '2021-01-10', '3'),
  ('A', '2021-01-11', '3'),
  ('A', '2021-01-11', '3'),
  ('B', '2021-01-01', '2'),
  ('B', '2021-01-02', '2'),
  ('B', '2021-01-04', '1'),
  ('B', '2021-01-11', '1'),
  ('B', '2021-01-16', '3'),
  ('B', '2021-02-01', '3'),
  ('C', '2021-01-01', '3'),
  ('C', '2021-01-01', '3'),
  ('C', '2021-01-07', '3');
 

CREATE TABLE menu (
  product_id INTEGER,
  product_name VARCHAR(5),
  price INTEGER
);

INSERT INTO menu
  (product_id, product_name, price)
VALUES
  ('1', 'sushi', '10'),
  ('2', 'curry', '15'),
  ('3', 'ramen', '12');
  

CREATE TABLE members (
  customer_id VARCHAR(1),
  join_date DATE
);

INSERT INTO members
  (customer_id, join_date)
VALUES
  ('A', '2021-01-07'),
  ('B', '2021-01-09');
  
  
  show tables
  
  
-- 1. What is the total amount each customer spent at the restaurant?
SELECT
  s.customer_id,
  SUM(m.price) AS total_spent
FROM sales AS s
INNER JOIN menu AS m
  ON s.product_id = m.product_id
GROUP BY
  s.customer_id
-- 2. How many days has each customer visited the restaurant?
SELECT
  customer_id,
  COUNT(DISTINCT order_date) AS visit_days
FROM sales
GROUP BY
  customer_id

-- 3. What was the first item from the menu purchased by each customer?
WITH CustomerFirstPurchase AS (
  SELECT
    s.customer_id,
    s.order_date,
    m.product_name,
    ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY s.order_date ASC) AS rn
  FROM sales AS s
  INNER JOIN menu AS m
    ON s.product_id = m.product_id
)
SELECT
  customer_id,
  product_name AS first_purchased_item
FROM CustomerFirstPurchase
WHERE
  rn = 1;

-- 4. What is the most purchased item on the menu and how many times was it purchased by all customers?
SELECT
  m.product_name,
  COUNT(s.product_id) AS total_purchases
FROM sales AS s
INNER JOIN menu AS m
  ON s.product_id = m.product_id
GROUP BY
  m.product_name
ORDER BY
  total_purchases DESC
LIMIT 1;

-- 5. Which item was the most popular for each customer?
WITH CustomerItemPurchaseCount AS (
  SELECT
    s.customer_id,
    m.product_name,
    COUNT(s.product_id) AS purchase_count,
    ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY COUNT(s.product_id) DESC) AS rn
  FROM sales AS s
  INNER JOIN menu AS m
    ON s.product_id = m.product_id
  GROUP BY
    s.customer_id,
    m.product_name
)
SELECT
  customer_id,
  product_name AS most_popular_item
FROM CustomerItemPurchaseCount
WHERE
  rn = 1;

-- 6. Which item was purchased first by the customer after they became a member?
WITH MemberFirstPurchase AS (
  SELECT
    s.customer_id,
    s.order_date,
    m.product_name,
    ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY s.order_date ASC) AS rn
  FROM sales AS s
  INNER JOIN menu AS m
    ON s.product_id = m.product_id
  INNER JOIN members AS mem
    ON s.customer_id = mem.customer_id
  WHERE
    s.order_date >= mem.join_date
)
SELECT
  customer_id,
  product_name AS first_item_as_member
FROM MemberFirstPurchase
WHERE
  rn = 1;

-- 7. Which item was purchased just before the customer became a member?
WITH PreMemberPurchase AS (
  SELECT
    s.customer_id,
    s.order_date,
    m.product_name,
    ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY s.order_date DESC) AS rn
  FROM sales AS s
  INNER JOIN menu AS m
    ON s.product_id = m.product_id
  INNER JOIN members AS mem
    ON s.customer_id = mem.customer_id
  WHERE
    s.order_date < mem.join_date
)
SELECT
  customer_id,
  product_name AS item_before_member
FROM PreMemberPurchase
WHERE
  rn = 1;

-- 8. What is the total items and amount spent for each member before they became a member?
SELECT
  s.customer_id,
  COUNT(s.product_id) AS total_items_before_member,
  SUM(m.price) AS total_amount_before_member
FROM sales AS s
INNER JOIN menu AS m
  ON s.product_id = m.product_id
INNER JOIN members AS mem
  ON s.customer_id = mem.customer_id
WHERE
  s.order_date < mem.join_date
GROUP BY
  s.customer_id
  
-- 9.  If each $1 spent equates to 10 points and sushi has a 2x points multiplier 
-- how many points would each customer have?
SELECT
  s.customer_id,
  SUM(CASE
    WHEN m.product_name = 'sushi' THEN m.price * 10 * 2
    ELSE m.price * 10
  END) AS total_points
FROM sales AS s
INNER JOIN menu AS m
  ON s.product_id = m.product_id
GROUP BY
  s.customer_id

-- 10. In the first week after a customer joins the program (including their join date) 
-- they earn 2x points on all items, not just sushi - how many points do customer A and B have 
-- at the end of January?
SELECT
  s.customer_id,
  SUM(
    CASE
      -- Condition 1: Customer is a member AND the order is within their first 7 days of joining (inclusive of join date)
      WHEN mem.join_date IS NOT NULL
           AND s.order_date >= mem.join_date
           AND s.order_date <= DATE_ADD(mem.join_date, INTERVAL 6 DAY) THEN m.price * 10 * 2 -- 2x points for all items
      -- Condition 2: Order is outside the first 7 days of membership OR before becoming a member
      -- In this case, apply the standard sushi multiplier
      WHEN m.product_name = 'sushi' THEN m.price * 10 * 2 -- Sushi gets 2x points
      ELSE m.price * 10 -- All other items get standard 1x points
    END
  ) AS total_points_january
FROM sales AS s
INNER JOIN menu AS m
  ON s.product_id = m.product_id
LEFT JOIN members AS mem
  ON s.customer_id = mem.customer_id
WHERE
  s.customer_id IN ('A', 'B') -- Focus only on customers A and B
  AND s.order_date <= '2021-01-31' -- Only consider sales up to the end of January
GROUP BY
  s.customer_id
ORDER BY
  s.customer_id;