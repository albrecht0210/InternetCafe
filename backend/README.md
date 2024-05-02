# Internet Cafe Queue System (Backend)

## Technology Used

1. Python
2. Django
3. Django Rest Framework
4. Django Simple JWT
5. XAMPP (or similar mysql services)
6. MySQL/SQLite

## Setup and Installing

### Setup
Update the .env file variables.
Copy the sample_env.txt to .env file.
```
DATABASE_NAME=your_database_name
DATABASE_USERNAME=username
DATABASE_PASSWORD=password
```

### Install
Run the following commands to the terminal.
```python
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuper (optional)
python manage.py runserver
```

## Models

```
Account
- string (uuid) | Id (PK)
- string        | First Name
- string        | Last Name
- string        | Username
- string        | Password
- boolean       | Is Superuser
```

```
Computer
- string (uuid) | Id (PK)
- string        | Name
- int           | Status (1=Available, 2=Pending, 3=In Use, 4=Maintenance)
- datetime      | Created At
```

```
Queue
- string (uuid) | Id (PK)
- string (uuid) | Account (FK)
- string (uuid) | Computer (FK)
- string        | Number
- int           | Status (1=Waiting, 2=Now Serving)
- datetime      | Created At
```

```
Session
- string (uuid) | Id (PK)
- string (uuid) | Account (FK)
- string (uuid) | Computer (FK)
- datetime      | Start Time
- datetime      | End Time
```
## API Urls

```
Authorization | Action | Url
```

### Authentication

```
Any  | POST | http://localhost:8000/api/token/
User | POST | http://localhost:8000/api/token/refresh/
User | POST | http://localhost:8000/api/token/verify/
```
 
### Account

```
Admin | GET            | http://localhost:8000/api/accounts/
Admin | POST           | http://localhost:8000/api/accounts/register/
User  | GET            | http://localhost:8000/api/accounts/profile/
Admin | GET,PUT,DELETE | http://localhost:8000/api/accounts/{id}/
```

### Computer
```
Admin | GET,POST       | http://localhost:8000/api/computers/
Admin | GET            | http://localhost:8000/api/computers/{available|pending|in_use|maintenance}/
Admin | PUT            | http://localhost:8000/api/computers/update_status/
Admin | GET,PUT,DELETE | http://localhost:8000/api/computers/{id}/
```

### Queue
```
Admin | GET            | http://localhost:8000/api/queues/
Admin | GET            | http://localhost:8000/api/queues/waiting/
Any   | GET            | http://localhost:8000/api/queues/now_serving/
User  | GET            | http://localhost:8000/api/queues/get_queue_number/
User  | POST           | http://localhost:8000/api/queues/queue_computer/
User  | POST           | http://localhost:8000/api/queues/dequeue_computer/
Admin | POST           | http://localhost:8000/api/queues/next_queue/
Admin | GET,DELETE     | http://localhost:8000/api/queues/{id}/
```

### Session
```
Admin | GET            | http://localhost:8000/api/sessions/
User  | GET            | http://localhost:8000/api/sessions/my_session/
User  | GET            | http://localhost:8000/api/sessions/my_all_session/
User  | POST           | http://localhost:8000/api/sessions/create_session/
User  | PUT            | http://localhost:8000/api/sessions/{id}/end_session/
Admin | GET,DELETE     | http://localhost:8000/api/sessions/{id}/
```