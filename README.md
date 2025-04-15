# Broccoli

A **Scalable E-commerce Platform** built with Django and PostgreSQL.
A basic set of functionalities allowing users to interact with the platform.

![Broccoli landing](https://raw.githubusercontent.com/alanchrissantony/Broccoli/main/assets/landing.png)
![Broccoli products](https://raw.githubusercontent.com/alanchrissantony/Broccoli/main/assets/products.png)

## Features

- **User Authentication**  
  Secure sign-up, login, and password reset powered by Django Allauth.

- **Product & Inventory Management**  
  Create, update, and delete products and categories; real‑time stock synchronization.

- **Shopping Cart & Checkout**  
  Add items to cart, proceed through checkout, and select payment methods (PayPal, Wallet, COD).

- **Order Management**  
  View order history, order status tracking, and email notifications on status changes.

- **Admin Dashboard**  
  Custom Django admin with enhanced UX for managing users, products, and orders.

- **Media Handling**  
  Cloudinary integration for optimized image uploads and delivery.

- **Performance Optimization**  
  Redis caching for product listings and homepage, ensuring fast page loads.

- **Security Best Practices**  
  CSRF protection, PBKDF2 password hashing, HTTPS enforcement, and JWT for API endpoints.


## Diagram DB

![Broccoli diagram DB](https://raw.githubusercontent.com/alanchrissantony/Broccoli/main/assets/db.svg)


## Installation and Running

1. Clone the repository to your local machine:

```bash
$ git clone https://github.com/alanchrissantony/Broccoli.git
```

2. Navigate to the project directory:

```bash
$ cd Broccoli
```

3. Create/Activate environment:

```bash
$ pip install virtualenv
$ python -m virtualenv venv
$ .\venv\Scripts\activate
$ # or linux
$ source venv/bin/activate
```

4. Install dependencies:

```bash
$ pip install -r requirements.txt
```

5. Apply migrations to create the database:

```bash
$ python manage.py migrate
```

6. Run the server:

```bash
$ python manage.py runserver
```

### If you want the api to send messages to mail

Then you MUST create and config `.env`.

For example I create `.env`

All these files are in [.env](.env)

You can now access the API in your browser at http://localhost:8000/.


## Custom Admin

![Spotify admin](https://raw.githubusercontent.com/alanchrissantony/Broccoli/main/assets/admin.png)

## Author

This project is developed by Alan Chris Antony.