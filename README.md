# Event Manager API

The Event Manager API is developed using Django REST Framework. It supports user registration, authentication with JWT (JSON Web Tokens), event management, and provides a comprehensive filtering system for events.
## Requirements

- Python v3.10
- Django v3.2 or newer
- Django REST Framework
- djangorestframework-simplejwt for JWT authentication

Ensure you have Python 3.10 installed on your system to work with this project effectively. This version requirement is due to specific language features and library support utilized in the project.


## Features

- User registration and authentication with JWT.
- Access and refresh token system with token rotation.
- CRUD operations for managing events.
- Event registration and deregistration for users.
- Filtering events by name, date, and other criteria.
- Swagger documentation for exploring API endpoints.

## Installation

### Clone the Repository

```bash
git clone git@github.com:Kucherenko1van/event_manager_project.git &&
cd event_manager_project
```

## Set Up a Virtual Environment

### For Linux/macOS:

```bash
python3 -m venv venv &&
source venv/bin/activate
```

### For Windows:

```bash
python3 -m venv venv
.\venv\Scripts\activate
```

## Install Dependencies

```bash
pip3 install -r requirements.txt
```

## Apply Migrations

```bash
python3 manage.py makemigrations &&
python3 manage.py migrate
```

## Create a Superuser

```bash
python3 manage.py createsuperuser
```

## Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.


## Running Tests

To run tests, execute:
```bash
python3 manage.py test
````

## Usage

### User Registration
POST `/register/`

Request body:

```json
{
  "username": "newuser",
  "password": "newpassword123",
  "email": "newuser@example.com"
}
```

### User Authentication
POST `/api/token/`

Request body:

```json
{
  "username": "newuser",
  "password": "newpassword123"
}
```

Response body:

```json
{
  "refresh": "REFRESH_TOKEN",
  "access": "ACCESS_TOKEN"
}
```

### Refreshing Access Token
POST `/api/token/refresh/`

Request body:

```json
{
  "refresh": "REFRESH_TOKEN"
}
```

Response body:

```json
{
  "access": "NEW_ACCESS_TOKEN"
}
```

### Managing Events

* Create an Event: POST `/events/` with event details in the request body.
* List Events: GET `/events/` to retrieve a list of events.
* Event Details: GET `/events/{event_id}/` to retrieve event details.
* Update an Event: PUT `/events/{event_id}/` with updated event details.
* Delete an Event: DELETE `/events/{event_id}/`.

### Filtering Events
GET `/events/?name={name}&start_date={date}&end_date={date}`

Replace `{name}`, `{start_date}`, and `{end_date}` with your filter criteria.

### Documentation
Visit `/swagger/` for interactive Swagger documentation and explore all API endpoints.

### Running Tests
To run tests, execute:

```bash
python3 manage.py test
```

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.