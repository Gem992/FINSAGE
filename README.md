# Finsage - Finance Tracker

A modern finance tracking application built with Django, featuring pie charts for income and expense distribution analysis.

## Features

- **User Authentication**: Secure signup and login system
- **Income & Expense Tracking**: Add and manage your financial transactions
- **Real-time Dashboard**: View total income, expenses, and net balance
- **Monthly Reports**: Track your current month's financial activity
- **Interactive Charts**: Pie charts showing income and expense distribution using matplotlib
- **Modern UI**: Beautiful Bootstrap-based interface with gradient backgrounds
- **Responsive Design**: Works perfectly on desktop and mobile devices

## Technology Stack

- **Backend**: Django 5.2.4
- **Database**: SQLite (can be configured for MySQL)
- **Frontend**: Bootstrap 5.3.0
- **Charts**: Matplotlib
- **Styling**: Custom CSS with inline styles

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project
```bash
# If you have the project files, navigate to the project directory
cd "path/to/finsage - Copy"
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Database Setup
The project uses SQLite by default (and only) for this setup. No additional database setup is required.

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run the Development Server
```bash
python manage.py runserver
```

### Step 7: Access the Application
Open your browser and navigate to:
- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Usage

### Getting Started
1. Visit the homepage and click "Sign Up" to create an account
2. Log in with your credentials
3. Start adding your income and expenses

### Adding Transactions
- **Income**: Click "Add Income" and enter the source and amount
- **Expenses**: Click "Add Expense" and enter the name and amount
- All transactions are automatically saved and reflected in real-time

### Viewing Charts
- Click "View Charts" on the dashboard to see pie charts
- Charts show the distribution of your income and expenses
- Charts are generated using matplotlib and displayed as images

### Monthly Reports
- The dashboard shows your current month's transactions
- Income and expenses are color-coded for easy identification

## Project Structure

```
finsage - Copy/
├── finsage_project/          # Django project settings
├── finance/                  # Main app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── index.html          # Homepage
│   ├── signup.html         # Registration page
│   ├── login.html          # Login page
│   ├── dashboard.html      # Main dashboard
│   └── charts.html         # Charts page
├── static/                 # Static files
├── manage.py              # Django management script
└── README.md              # This file
```

## Key Features Implemented

### 1. Pie Charts with Matplotlib
- Income distribution pie chart
- Expense distribution pie chart
- Charts are generated server-side and embedded as base64 images
- Automatic updates when new data is added

### 2. Django Backend
- Complete user authentication system
- RESTful API endpoints for adding income/expenses
- Database models for Income and Expense
- Session-based authentication

### 3. Bootstrap Styling
- Modern gradient backgrounds
- Responsive design
- Custom button styles with hover effects
- Card-based layout with glassmorphism effects
- Inline CSS for better performance

### 4. Database Integration
- SQLite database (uses `db.sqlite3` in the project root)

## Customization

### Changing Database
This project is configured for SQLite only. MySQL instructions and scripts have been removed.

### Adding New Features
- Models: Add to `finance/models.py`
- Views: Add to `finance/views.py`
- URLs: Add to `finance/urls.py`
- Templates: Create in `templates/` directory

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Run migrations to create the SQLite database: `python manage.py migrate`
   - Verify `DATABASES` in `finsage_project/settings.py` points to SQLite (default)

2. **Migration Errors**
   - Run `python manage.py makemigrations`
   - Then `python manage.py migrate`

3. **Static Files Not Loading**
   - Run `python manage.py collectstatic`

4. **Chart Generation Issues**
   - Ensure matplotlib is installed: `pip install matplotlib`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please create an issue in the repository or contact the development team. 