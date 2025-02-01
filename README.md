## Carwash Business Admin Panel API
This project is a backend API for managing a carwash business admin panel, built with Django. It allows the admin to manage carwash services, customer data, payments, and more.

### Features
- **User authentication**: Allows for admin and staff logins.
- **Carwash services management**: Add, update, and delete services.
- **Customer management**: Keep track of customer data and service history.
- **Payment processing**: Record payments for services.
- **API documentation**: Expose RESTful APIs for each resource (using Django REST Framework).

### Requirements
- Python 3.13.1 or later
- Django 4.0 or later
- Django REST Framework
- MySQL (or another database if preferred)

### Installation
1. Clone Repository
```bash
git clone https://github.com/markmamba/carwash_system.git
cd carwash_system
```
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up the database
  Make sure you have MySQL (or another preferred database) set up. Then, update the `DATABASES` settings in `settings.py` if needed.
5. Run migrations
```bash
python manage.py migrate
```
6. Start the development server
```bash
python manage.py runserver
```
The server will start at `http://127.0.0.1:8000/`.
