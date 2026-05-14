# SubTrack - Subscription Management System

A modern, web-based subscription management system built with **Flask** and **MySQL**. SubTrack helps businesses manage subscribers, subscription plans, payments, and invoices efficiently through an intuitive web interface.

## 🎯 Features

- **Dashboard**: Real-time metrics including total subscribers, active subscriptions, and revenue tracking
- **Subscriber Management**: Add, view, and manage customer information
- **Subscription Plans**: Create and manage multiple subscription tiers with different pricing
- **Payment Tracking**: Record and monitor payments with status tracking (Pending, Successful)
- **Invoice Management**: Automated invoice generation and payment status updates
- **Expiring Subscriptions**: Quick view of subscriptions expiring soon
- **Multi-tenant Ready**: Built with tenant support for future scalability

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS, Jinja2 Templates
- **Server**: Gunicorn (production)
- **Environment**: Python 3.8+

## 📋 Requirements

- Python 3.8 or higher
- MySQL Server running locally or remotely
- pip (Python package manager)

## ⚙️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/SubTrack.git
cd SubTrack
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root and configure your database connection:
```
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=SubscriptionDB
SECRET_KEY=your_secret_key_here
```

### 5. Set Up Database
Create the MySQL database and tables (database schema file should be imported):
```bash
# In MySQL client:
CREATE DATABASE SubscriptionDB;
# Import your schema file
mysql -u root -p SubscriptionDB < schema.sql
```

### 6. Run the Application
```bash
# Development server
python -m flask run

# Production server (using Gunicorn)
gunicorn app:app
```

The application will be available at `http://127.0.0.1:5000`

## 📁 Project Structure

```
SubTrack/
├── app.py                 # Main Flask application
├── db.py                  # Database connection and utilities
├── requirements.txt       # Python dependencies
├── Procfile              # Production configuration (Heroku/similar)
├── .env                  # Environment variables (DO NOT commit)
├── .gitignore            # Git ignore rules
├── static/
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript files
└── templates/
    ├── base.html         # Base template
    ├── dashboard.html    # Dashboard page
    ├── subscribers.html  # Subscribers list
    ├── add_subscriber.html
    ├── plans.html        # Subscription plans
    ├── add_plan.html
    ├── payments.html     # Payments list
    ├── add_payment.html
    ├── subscriptions.html # Subscriptions list
    ├── add_subscription.html
    └── ...
```

## 🚀 Key Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Dashboard with analytics |
| `/subscribers` | GET | List all subscribers |
| `/subscribers/add` | GET, POST | Add new subscriber |
| `/subscribers/delete/<id>` | GET | Delete subscriber |
| `/plans` | GET | List subscription plans |
| `/plans/add` | GET, POST | Add new plan |
| `/payments` | GET | List all payments |
| `/payments/add` | GET, POST | Record new payment |
| `/subscriptions` | GET | List all subscriptions |
| `/subscriptions/add` | GET, POST | Create new subscription |

## 🔒 Security Notes

- **DO NOT** commit `.env` file to version control (it's in `.gitignore`)
- Use strong passwords for database credentials
- Change the `SECRET_KEY` to a secure random value in production
- Always use environment variables for sensitive data
- Consider using HTTPS in production

## 📝 Database Schema

The application expects the following main tables:
- `User` - Customer information
- `Subscription_Plan` - Available subscription tiers
- `User_Subscription` - Active subscriptions linked to users
- `Invoice` - Generated invoices
- `Payment` - Payment records

## 🐛 Troubleshooting

### MySQL Connection Error
- Ensure MySQL server is running
- Verify credentials in `.env` file
- Check database exists and user has permissions

### Module Not Found Error
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Port Already in Use
- Default Flask port is 5000. Change it:
  ```bash
  python -m flask run --port 5001
  ```

## 📦 Dependencies

See [requirements.txt](requirements.txt) for complete list:
- Flask 3.1.3
- mysql-connector-python 9.6.0
- python-dotenv 1.2.2
- Gunicorn 25.3.0
- Jinja2 3.1.6

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

---

**Last Updated**: April 2026
