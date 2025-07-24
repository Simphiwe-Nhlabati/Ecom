# 🛒 Django E-Commerce Platform

A feature-rich e-commerce platform built with Django that supports buyers and vendors. Vendors can list products, while buyers can browse, add to cart, and purchase products. The backend is powered by SQL (MariaDB, MySQL, or PostgreSQL).

## 🚀 Features

- 🔐 User registration with roles: Buyer & Vendor
- 🛍️ Product listing, editing, and deletion (by vendors)
- 🛒 Cart functionality (add/update/remove items)
- 💳 Checkout system with order summary and confirmation
- 📊 Sales report for vendors
- 🗃️ SQL database (MariaDB, PostgreSQL, or MySQL)
- ✅ Admin panel for site management

## 📦 Tech Stack

- **Backend**: Django 4.x, Python 3.10+
- **Frontend**: Bootstrap 5, HTML/CSS
- **Database**: SQL; MySQL
- **Authentication**: Django built-in
- **APIs**: Django REST Framework 


## 🗃️ API(Endpoints)

- **Create new stores**:api/generate_store_api/
- **Create new products**: api/generate_product_api/
- **Reviews**: api/list_review/

---

## ⚙️ Setup Instructions

### 🖥️ Prerequisites

- Python 3.10+
- Django 4.x
- pip
- SQL database (MariaDB/MySQL/PostgreSQL)

### 📥 Installation

```bash

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start the development server
python manage.py runserver
