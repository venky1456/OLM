# Online Library Management System (OLMS)

A comprehensive Django-based library management system with full frontend and backend implementation, featuring role-based access control for administrators and students.

## 🚀 Features

### Core Functionality
- **User Management**: Separate login for Admin and Students
- **Book Management**: Add, edit, delete, and search books
- **Issue/Return System**: Complete book lending workflow
- **Category Management**: Organize books by categories
- **Search & Filter**: Advanced search functionality
- **Dashboard**: Role-specific dashboards with statistics

### Admin Features
- Complete book management (CRUD operations)
- Student account management
- Issue and return books
- Transaction history and reports
- Category management
- Overdue book tracking

### Student Features
- Browse available books
- Search books by title, author, ISBN, category
- Request book issues
- View borrowing history
- Check due dates and fines

### Technical Features
- Responsive Bootstrap 5 UI
- Role-based access control
- Form validation
- Pagination
- AJAX search functionality
- Image upload for book covers
- Export/Print functionality

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**
- **Django 5.2.3**
- **SQLite** (can be configured for PostgreSQL)
- **Pillow** (for image handling)

### Frontend
- **HTML5/CSS3**
- **Bootstrap 5.3.0**
- **JavaScript/jQuery**
- **FontAwesome 6.4.0**

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd OLM
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install django pillow
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser and Sample Data
```bash
python create_superuser.py
python create_sample_data.py
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access the Application
Open your browser and navigate to: `http://127.0.0.1:8000/`

## 👤 Default Login Credentials

### Admin User
- **Username:** admin
- **Password:** admin123
- **Email:** admin@olms.com

### Sample Students
- **Username:** john_doe, **Password:** student123
- **Username:** jane_smith, **Password:** student123
- **Username:** mike_wilson, **Password:** student123

## 📁 Project Structure

```
OLM/
├── olms/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── library/                # Main application
│   ├── __init__.py
│   ├── admin.py           # Admin interface configuration
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL patterns
│   └── forms.py           # Django forms
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard_admin.html    # Admin dashboard
│   ├── dashboard_student.html  # Student dashboard
│   ├── book_list.html     # Book management
│   ├── book_detail.html   # Book details
│   └── contact.html       # Contact page
├── static/                 # Static files
│   ├── css/
│   │   └── style.css      # Custom CSS
│   ├── js/
│   │   └── main.js        # Custom JavaScript
│   └── images/
├── media/                  # User uploaded files
├── manage.py              # Django management script
├── create_superuser.py    # Superuser creation script
├── create_sample_data.py  # Sample data population script
└── README.md              # This file
```

## 🗄️ Database Models

### UserProfile
- Extends Django User model
- User type (admin/student)
- Contact information
- Address

### Category
- Book categories
- Description

### Book
- Title, author, ISBN
- Category, description
- Publication details
- Inventory management
- Cover image

### IssueTransaction
- Book lending transactions
- Issue/return dates
- Fine calculation
- Status tracking

### BookRequest
- Student book requests
- Request status management

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration
The system uses SQLite by default. To use PostgreSQL:

1. Install psycopg2: `pip install psycopg2-binary`
2. Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'olms_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### Production Setup

1. **Set Debug to False**
   ```python
   DEBUG = False
   ```

2. **Configure Allowed Hosts**
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

3. **Static Files**
   ```bash
   python manage.py collectstatic
   ```

4. **Database**
   - Use PostgreSQL for production
   - Run migrations: `python manage.py migrate`

5. **Web Server**
   - Use Gunicorn: `pip install gunicorn`
   - Configure Nginx as reverse proxy

### Docker Deployment
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "olms.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📝 API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /register/` - User registration
- `GET /logout/` - User logout

### Books
- `GET /books/` - List all books (admin)
- `GET /student/books/` - List available books (student)
- `GET /books/<id>/` - Book details
- `POST /books/add/` - Add new book (admin)
- `PUT /books/<id>/edit/` - Edit book (admin)
- `DELETE /books/<id>/delete/` - Delete book (admin)

### Transactions
- `GET /transactions/` - List transactions (admin)
- `POST /issue-book/` - Issue book (admin)
- `POST /return-book/<id>/` - Return book (admin)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact: admin@olms.com

## 🔄 Version History

- **v1.0.0** - Initial release with core functionality
- Role-based access control
- Book management system
- Issue/return workflow
- Responsive UI

## 🎯 Roadmap

- [ ] Email notifications
- [ ] Advanced reporting
- [ ] Mobile app
- [ ] Integration with external book APIs
- [ ] Multi-language support
- [ ] Advanced search filters
- [ ] Book recommendations
- [ ] QR code integration

---

**Developed with ❤️ using Django and Bootstrap** 