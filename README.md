# django-ecommerce-api
An E-commerce API built using Django Rest Framework. 

## About Project
The project has 5 local Apps:
- Users
- Products
- Orders
- Checkouts

## Basic Feature
- Registration using either phone and email (Activate account by email)
- Login system with Json Web Token(JWT)
     - Login with email, password
     - Login with phone number(send SMS code)
- Password change and reset endpoints.
- Custom permissions set for necessary endpoints(for each app)
- Payment system using [Zarinpal](https://github.com/rasooll/zarinpal-django-py3/) and [IDpay](https://github.com/idpay/idpay-django-project)
- Documentation using Swagger UI

## Built with
- Django
- Django Rest Framework

## Technologies Used
- PostgreSQL
- Celery

## ER Diagram
Database Relationship diagram generated using [dbdiagram](https://dbdiagram.io/home)
> [Entity-Relationship link](https://dbdiagram.io/d/E-commerce-6561c3da3be1495787b58a33)
![E-commerce](https://github.com/shahriar-fattahi/django-ecommerce-api/assets/109045277/4d650bd8-3db8-4c4c-82ff-6a8ffc2afe99)

## Getting Started
1. Clone this repository to your local machine:
```
git clone https://github.com/shahriar-fattahi/django-ecommerce-api
```
2. Rename the **.env.example** file found in the root directory of the project to .env and update the environment variables accordingly.

4. Create a Virtual Environment:
```
python -m venv your_venv_name
```
4. Install Requirements:
```
pip install -r requirements.txt
```
