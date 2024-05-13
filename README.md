Vendor-Management-System
==========

Vendor-Management-System API is a RESTful API for managing vendors and purchase orders.

Features
Create, read, update, and delete vendors
Create, read, update, and delete purchase orders
Retrieve vendor performance metrics
Filter purchase orders by vendor
Getting Started
To get started with Vendor-Management-System API, follow these steps:

Installation
------------

**Requirements:**
- Python 3.9.11

**Steps:**
Clone the repository:

```
git clone https://github.com/Nikunj6265/Vendor-Management-System.git
```
Install dependencies:

```
cd Vendor-Management-System
pip install -r requirements.txt
```
Run migrations:

```
python manage.py makemigrations
python manage.py migrate
```
Create a superuser:
```
python manage.py createsuperuser
```
Start the development server:
```
python manage.py runserver
```
Access the API at http://127.0.0.1:8000/api/

Follow the Document and Postman Dump to understand each API endpoint thoroughly.

Document Link: https://drive.google.com/file/d/1lSpEphGS7m5Bxc73fvGidYzlpVovPCNd/view?usp=sharing

Postman Dump Link: https://drive.google.com/file/d/13MMefy9BCYIBkHekQK60UY3vgSa03cbh/view?usp=sharing

