# Django REST API with Role-Based Access Control

A Django REST API implementation featuring JWT authentication, role-based access control, and team management functionality.

## Features

- JWT-based authentication using `djangorestframework-simplejwt`
- Role-based access control (Admin, Manager, User)
- Team management system
- Containerized application using Docker
- PostgreSQL database integration
- API documentation using Swagger/ReDoc


## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/SaadZahidQureshi/Django-Rest-Project.git
cd dDjango-Rest-Project
```

2. Create a `.env` file in the project root:
```bash
DEBUG=1
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_dev
SQL_USER=django_user
SQL_PASSWORD=django_password
SQL_HOST=db
SQL_PORT=5432
```

3. Build and run the containers:
```bash
docker-compose up --build
```

4. Create a superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Authentication
- `POST api/token/` - Obtain JWT token
- `POST api/token/refresh/` - Refresh JWT token

### User Management
- `GET api/admin/` - Admin endpoint to list all users (Admin only)
- `GET api/manager/` - List users for manager's team
- `GET api/manager/<int:pk>/` - Retrieve/Update specific user in manager's team
- `GET api/user/` - View/Update user's own profile

### Team Management
- `GET api/team` - List teams
- `POST api/team` - Create new team
- `GET api/team/<id>` - Retrieve team details
- `PUT api/team/<id>` - Update team
- `DELETE api/team/<id>` - Delete team


### API Documentation
The API documentation is available at:
```
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
