```markdown
# 🛍️ Jumia-Like E-commerce App (Flask + MySQL + Docker + M-Pesa STK Push)

A simple yet functional **Jumia-like online shop** built using **Flask**, **MySQL**, and **Safaricom Daraja STK Push API** for seamless mobile payments — now containerized with **Docker** for easy setup and deployment.

This project demonstrates **real-world e-commerce features**, **database integration**, and **mobile payment automation** using Python and Docker.

---

## 🚀 Features

- 🧍 User Registration & Login (Session-based authentication)
- 🛒 Browse Products by Category (Smartphones, Clothes, Bags, etc.)
- 📦 View Single Product Details & Similar Products
- 💳 M-Pesa STK Push Payment Integration (Daraja API)
- 🗃️ MySQL Database (Users, Products, Orders)
- 🧱 Dockerized Setup for Flask + MySQL
- 🔐 Logout & Session Management
- 🧰 Flask Backend with Jinja2 Templates and Bootstrap Styling

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Flask (Python) |
| **Database** | MySQL 8.x |
| **Containerization** | Docker + Docker Compose |
| **Frontend** | HTML, CSS, Bootstrap (Jinja2 templates) |
| **Payments** | M-Pesa Daraja STK Push API |
| **Environment** | Python 3.x |
| **Deployment** | Dockerized / PythonAnywhere / Render |

---

jumia-flask/
│
├── static/                  # CSS, JS, and image files
│   ├── style.css
│   └── images/
│
├── templates/               # HTML templates (home, single, signup, signin)
│   ├── index.html
│   ├── single.html
│   ├── signup.html
│   ├── signin.html
│   └── payment.html
│
├── app.py                   # Main Flask application
├── derrick.sql              # SQL script to initialize MySQL/PostgreSQL database
├── Dockerfile               # Docker configuration for Flask container
├── docker-compose.yml       # Defines multi-container setup (Flask + DB)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


---

## 🐳 Docker Setup

### 1️⃣ Create a `Dockerfile`

```dockerfile
# Use official lightweight Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
````

---

### 2️⃣ Create `docker-compose.yml`

```yaml
version: "3.8"

services:
  db:
    image: mysql:8.0
    container_name: jumia_db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: jumia
      MYSQL_USER: flaskuser
      MYSQL_PASSWORD: flaskpass
    ports:
      - "3306:3306"
    volumes:
      - ./derrick.sql:/docker-entrypoint-initdb.d/derrick.sql
    restart: always

  web:
    build: .
    container_name: jumia_app
    depends_on:
      - db
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=mysql+pymysql://flaskuser:flaskpass@db:3306/jumia
      - FLASK_ENV=development
    command: python app.py
```

---

### 3️⃣ Requirements (`requirements.txt`)

```txt
Flask
PyMySQL
requests
python-dotenv
```

---

### 4️⃣ Running the App

1. **Build and Start the containers**

   ```bash
   docker-compose up --build
   ```

2. Visit the app at:
   👉 [http://localhost:5000](http://localhost:5000)

3. **Stop containers**

   ```bash
   docker-compose down
   ```

4. (Optional) Run detached:

   ```bash
   docker-compose up -d
   ```

---

## 🗄️ Database Initialization

The MySQL container automatically initializes using your SQL dump file `derrick.sql`.

### Example `derrick.sql`

```sql
DROP TABLE IF EXISTS products, users;

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    product_desc TEXT,
    product_price DECIMAL(10,2),
    product_category VARCHAR(50),
    product_image VARCHAR(100)
);

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100),
    phone VARCHAR(20),
    password VARCHAR(100)
);

INSERT INTO products (product_name, product_desc, product_price, product_category, product_image) VALUES
('Samsung Galaxy A04', 'Smartphone', 17000, 'Smartphones', 'samsung_a04.jpg'),
('Omo Detergent', 'Cleaning detergent', 80, 'Detergents', 'omo.jpg'),
('Leather Backpack', 'Stylish brown leather bag', 1500, 'Bags', 'bag1.jpg');
```

---

## 🧠 Flask App Overview

The app uses **Flask + PyMySQL** to connect to the database via an environment variable:

```python
import os, pymysql
from flask import Flask, render_template, request, redirect, session, flash, url_for

app = Flask(__name__)
app.secret_key = 'jumia_secret_key'

def get_connection():
    return pymysql.connect(
        host='db',
        user='flaskuser',
        password='flaskpass',
        database='jumia',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return render_template('index.html', products=products)
```

> The `DATABASE_URL` is automatically set from Docker Compose.

---

## 💳 M-Pesa STK Push Integration

The app integrates with **Safaricom Daraja API** to trigger an STK Push for mobile payments.

### 🔁 Payment Flow

1. User enters their **phone number** and **amount**.
2. Flask app requests an **access token** from the Daraja API.
3. It generates a **base64-encoded password** using your shortcode, passkey, and timestamp.
4. Sends a request to `https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest`.
5. The user receives an M-Pesa prompt to complete payment.

### ⚙️ Environment Variables

You can use `.env` to store sensitive credentials:

```
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
PASSKEY=your_passkey
SHORTCODE=174379
```

---

## 📸 Key Routes

| Route                  | Method   | Description                    |
| ---------------------- | -------- | ------------------------------ |
| `/`                    | GET      | Homepage with product listings |
| `/single/<product_id>` | GET      | View single product details    |
| `/signup`              | GET/POST | Register new user              |
| `/signin`              | GET/POST | User login                     |
| `/logout`              | GET      | Logout                         |
| `/mpesa`               | POST     | STK push payment route         |

---

## 🧪 Testing the App

1. Use **Daraja Sandbox credentials** from [Safaricom Developer Portal](https://developer.safaricom.co.ke/).
2. Enter phone number like `2547XXXXXXXX` and amount `1`.
3. Check your M-Pesa simulator for STK confirmation.

---

## 🧠 Skills Demonstrated

* Flask Routing & Template Rendering
* MySQL Schema Design with PyMySQL
* REST API Integration (Daraja API)
* Docker Compose for Multi-Service Deployment
* Environment Variable Configuration
* Session Authentication and Flash Messages
* Bootstrap-based Frontend Layout

---

## 👨‍💻 Author

**Cephas N. Okuku**
📧 Email: [okungusefa@gmail.com](mailto:okungusefa@gmail.com)
🐙 GitHub: [okukucephasna](https://github.com/okukucephasna)
🔗 LinkedIn: [cephas-okuku](https://linkedin.com/in/cephas-okuku)

---

## 🧾 License

This project is licensed under the **MIT License** — feel free to use or modify it for your own learning or development.

---

> *“Code, containerize, and connect — your Flask app can scale as far as your creativity takes it.”*

It would include an alternate `docker-compose.postgres.yml` and connection helper.
```
