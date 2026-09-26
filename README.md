# ProShop

A professional Django-based e-commerce web application built with Python and Django.

## Features

- Product listing and product details
- Product images
- Shopping cart
- Checkout system
- Order management
- Customer order history
- User registration and login
- User profile
- Django admin panel
- Product management
- Responsive web interface

## Technology Stack

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Pillow

## Project Structure

- accounts/ - User registration, login, profile and authentication
- core/ - Core website functionality and homepage
- products/ - Products and product management
- orders/ - Cart, checkout, orders and order history
- proshop/ - Main Django project configuration
- templates/ - Website templates
- static/ - CSS and static files
- media/ - Product images
- manage.py - Django management utility

## Installation

Install the required packages:

pip install -r requirements.txt

Apply database migrations:

python manage.py migrate

Start the development server:

python manage.py runserver

Open the website:

http://127.0.0.1:8000/

## Admin Panel

Admin URL:

http://127.0.0.1:8000/admin/

Create an administrator with:

python manage.py createsuperuser

## Important Notes

- The project uses SQLite for the database.
- Product images are stored in the media/ directory.
- requirements.txt contains the required Python packages.
- Production deployment requires appropriate email, HTTPS, ALLOWED_HOSTS and secure-cookie configuration.

## Development Check

python manage.py check

