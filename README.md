# FastAPI Todo List Application

A full-stack todo list application built with FastAPI backend and vanilla HTML/CSS/JavaScript frontend. This project demonstrates modern web development practices including authentication, role-based access control, and RESTful API design.

## Features

### 🔐 Authentication & Authorization
- User registration and login system
- JWT token-based authentication
- Role-based access control (Admin/User roles)
- Password change functionality
- Phone number updates

### ✅ Todo Management
- Create, read, update, and delete todos
- Priority levels for todos
- Mark todos as completed/incomplete
- User-specific todo lists
- Admin can view and manage all todos

### 👥 User Management
- User profile management
- Admin dashboard for user oversight
- Phone number validation and updates
- Secure password handling

### 🎨 Frontend Features
- Responsive HTML/CSS/JavaScript interface
- Login and registration pages
- Todo management interface
- Edit todo functionality
- Clean, modern UI design

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation and settings management
- **OAuth2** - Authentication and authorization
- **JWT** - Token-based authentication
- **SQLAlchemy** - Database ORM (assumed)
- **Uvicorn** - ASGI web server

### Frontend
- **HTML5** - Markup structure
- **CSS3** - Styling and responsive design
- **Vanilla JavaScript** - Interactive functionality
- **Fetch API** - HTTP requests to backend

## Prerequisites

- Python 3.8+
- Modern web browser
- pip or pipenv for package management

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd fastapi-todo-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file):
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Usage

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the application:
   - **Homepage**: http://127.0.0.1:8000
   - **Login Page**: http://127.0.0.1:8000/auth/login-page
   - **Register Page**: http://127.0.0.1:8000/auth/register-page
   - **Todo Dashboard**: http://127.0.0.1:8000/todo/todo-page
   - **API Documentation**: http://127.0.0.1:8000/docs

## API Endpoints

### 🏠 General
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Homepage/Test endpoint |
| GET | `/healthy` | Health check |

### 🔐 Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/auth/login-page` | Render login page | ❌ |
| GET | `/auth/register-page` | Render register page | ❌ |
| POST | `/auth/auth` | Create new user | ❌ |
| POST | `/auth/login` | User login (get JWT token) | ❌ |
| GET | `/auth/showusers` | List all users | ❌ |
| POST | `/auth/updateuser` | Update user information | ❌ |

### ✅ Todo Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/todo/todo-page` | Render todo dashboard | ❌ |
| GET | `/todo/addtodo-page` | Render add todo page | ❌ |
| GET | `/todo/edit-todo-page/{todo_id}` | Render edit todo page | ❌ |
| GET | `/todo/` | Get all user todos | ✅ |
| GET | `/todo/{todo_id}` | Get specific todo | ✅ |
| POST | `/todo/add` | Create new todo | ✅ |
| PUT | `/todo/udate/{todo_id}` | Update todo | ✅ |
| DELETE | `/todo/delete/{todo_id}` | Delete todo | ✅ |

### 👑 Admin Features
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/admin/showusers` | Get all users (admin) | ✅ |
| GET | `/admin/showtodos` | Get all todos (admin) | ✅ |
| DELETE | `/admin/todo/delete/{todo_id}` | Delete any todo (admin) | ✅ |

### 👤 User Profile
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/user/getuser` | Get current user info | ✅ |
| PUT | `/user/changepassword` | Change user password | ✅ |
| PUT | `/user/updatephonenumber/{phonenumber}` | Update phone number | ✅ |

## Data Models

### User Registration (`Createuser`)
```json
{
  "username": "string",
  "email": "string",
  "firstname": "string",
  "lastname": "string",
  "password": "string",
  "role": "string",
  "phone_number": "string (min 10 chars)"
}
```

### Todo Request (`Todorequest`)
```json
{
  "title": "string (min 3 chars)",
  "description": "string (min 3 chars)",
  "priority": "integer (> 0)",
  "completed": "boolean"
}
```

### Authentication Token (`Token`)
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## Example Usage

### Register a New User
```bash
curl -X POST "http://127.0.0.1:8000/auth/auth" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "firstname": "John",
       "lastname": "Doe",
       "password": "password123",
       "role": "user",
       "phone_number": "1234567890"
     }'
```

### Login and Get Token
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=johndoe&password=password123"
```

### Create a Todo (with authentication)
```bash
curl -X POST "http://127.0.0.1:8000/todo/add" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Complete the todo app tutorial",
       "priority": 1,
       "completed": false
     }'
```

## Project Structure

```
fastapi-todo-app/
├── main.py                 # FastAPI application entry point
├── routers/               
│   ├── auth.py            # Authentication routes
│   ├── todo.py            # Todo management routes
│   ├── admin.py           # Admin-specific routes
│   └── user.py            # User profile routes
├── models/
│   ├── __init__.py
│   ├── user.py            # User database models
│   └── todo.py            # Todo database models
├── schemas/
│   ├── __init__.py
│   ├── user.py            # User Pydantic schemas
│   └── todo.py            # Todo Pydantic schemas
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   ├── js/
│   │   └── main.js        # Frontend JavaScript
│   └── images/            # Static images
├── templates/
│   ├── auth/
│   │   ├── login.html     # Login page
│   │   └── register.html  # Registration page
│   ├── todo/
│   │   ├── todo.html      # Todo dashboard
│   │   ├── add.html       # Add todo page
│   │   └── edit.html      # Edit todo page
│   └── base.html          # Base template
├── database.py            # Database configuration
├── dependencies.py        # FastAPI dependencies
├── security.py           # Authentication utilities
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **Role-Based Access**: Different permissions for users and admins
- **Input Validation**: Pydantic models for request validation
- **Phone Number Validation**: Minimum length requirements
- **CORS Protection**: Configured for secure cross-origin requests

## What I Learned

This comprehensive project taught me:

### Backend Development
- **FastAPI Framework**: Building modern, fast APIs with Python
- **Authentication Systems**: JWT tokens, OAuth2, password hashing
- **Database Design**: User and todo models with relationships
- **API Security**: Protected routes, role-based access control
- **Data Validation**: Pydantic models for request/response validation
- **Error Handling**: Proper HTTP status codes and error responses

### Frontend Development
- **Vanilla JavaScript**: Working with APIs using Fetch
- **HTML Templates**: Creating dynamic, responsive layouts
- **CSS Styling**: Modern, clean interface design
- **Form Handling**: User input validation and submission
- **Authentication Flow**: Managing login states and tokens

### Full-Stack Integration
- **API Communication**: Frontend-backend data exchange
- **Authentication Flow**: Login, registration, and protected routes
- **State Management**: Handling user sessions and data
- **Responsive Design**: Mobile-friendly interfaces

## Dependencies

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
sqlalchemy==2.0.23
python-dotenv==1.0.0
```

## Future Enhancements

- [ ] Database migrations with Alembic
- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Todo categories and tags
- [ ] Due dates and reminders
- [ ] File attachments for todos
- [ ] Real-time notifications
- [ ] Export todos to PDF/CSV
- [ ] Dark mode toggle
- [ ] Progressive Web App (PWA) features
- [ ] Docker containerization
- [ ] API rate limiting
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [JWT Authentication Guide](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [HTML/CSS/JavaScript Tutorials](https://developer.mozilla.org/en-US/docs/Web)
