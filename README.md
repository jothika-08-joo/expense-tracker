# 💰 Expense Tracker — Personal Finance Manager

A full-stack **Flask + SQLite** web application to track personal expenses with user authentication, category management, and monthly spending analytics.

📁 **GitHub:** [github.com/jothika-08-joo/expense-tracker](https://github.com/jothika-08-joo/expense-tracker)

---

## 📌 About

Expense Tracker is a full-stack web application built with Python and Flask. It allows users to register, log in, and track their daily expenses by category. The dashboard shows total expenses, current month spending, and a category-wise breakdown with percentage analysis.

The project demonstrates real-world backend concepts including user authentication using Flask-Login, SQLAlchemy ORM for database operations, relational database design with three connected models (User, Expense, Category), and Jinja2 template inheritance.

---

## ✨ Features

- 🔐 **User Authentication** — Register and login with password hashing using Werkzeug
- 📊 **Dashboard Analytics** — Total expenses, monthly total, and category-wise spending with percentage
- 🗂️ **Category Management** — Add, edit, and delete expense categories
- 💸 **Expense CRUD** — Create, read, update, and delete expenses
- 🔒 **Data Isolation** — Users can only access their own expenses
- 🎨 **Bootstrap 5 UI** — Clean and responsive interface

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Auth | Flask-Login, Werkzeug |
| Frontend | HTML, Bootstrap 5, Jinja2 |

---

## 🗄️ Database Schema

```python
# Three models with relationships

class User(db.Model):
    id       → Integer, Primary Key
    username → String(100), Unique, Not Null
    password → String(200), Not Null  # stored as hash

class Category(db.Model):
    id          → Integer, Primary Key
    name        → String(100), Unique, Not Null
    description → String(200)
    expenses    → Relationship with Expense model

class Expense(db.Model):
    id          → Integer, Primary Key
    title       → String(100), Not Null
    amount      → Float, Not Null
    date        → String(20), Not Null
    user_id     → Foreign Key → users.id
    category_id → Foreign Key → category.id
```

---

## 🔁 Application Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home — redirects to login |
| `/register` | GET, POST | Register new user |
| `/login` | GET, POST | Login existing user |
| `/logout` | GET | Logout and redirect to login |
| `/dashboard` | GET | Show all expenses + analytics |
| `/add` | GET, POST | Add new expense |
| `/edit/<id>` | GET, POST | Edit existing expense |
| `/delete/<id>` | GET | Delete an expense |
| `/categories` | GET | List all categories |
| `/categories/add` | GET, POST | Add new category |
| `/categories/edit/<id>` | GET, POST | Edit a category |
| `/categories/delete/<id>` | GET | Delete a category |

---

## 📁 Project Structure

```
expense-tracker/
├── app.py              ← All routes and business logic
├── models.py           ← Database models (User, Expense, Category)
├── requirements.txt    ← Python dependencies
└── templates/
    ├── base.html           ← Parent layout with Bootstrap
    ├── login.html          ← Login page
    ├── register.html       ← Register page
    ├── dashboard.html      ← Main dashboard with analytics
    ├── add_expense.html    ← Add expense form
    ├── edit_expense.html   ← Edit expense form
    ├── categories.html     ← Category list
    └── add_category.html   ← Add/Edit category form
```

---

## 🚀 Getting Started

### Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/jothika-08-joo/expense-tracker.git
cd expense-tracker

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

App will be running at `http://localhost:5000`

> SQLite database (`database.db`) is created automatically on first run — no setup needed!

---

## 📦 Requirements

```
Flask
Flask-Login
Flask-SQLAlchemy
Werkzeug
```

---

## 🔐 Security Features

- Passwords never stored as plain text — hashed using `werkzeug.security.generate_password_hash`
- Login verified using `check_password_hash`
- All routes protected with `@login_required` from Flask-Login
- Expense edit and delete checks `expense.user_id != current_user.id` — users cannot access other users' data

---

## 📊 Dashboard Features

The dashboard calculates and displays:
- **Total expenses** — sum of all expenses for the logged-in user
- **This month** — sum of expenses in the current month only
- **Total transactions** — count of all expense entries
- **Category-wise table** — each category total + percentage of overall spending

---

## 📸 Screenshots

### Login Page
![Login Page](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/login_page.png)

### Register Page
![Register Page](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/register.png)

### Dashboard
![Dashboard](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/dashboard.png)

### Add Expense
![Add Expense](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/add_expense.png)

### Add Categories
![Add Categories](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/add_categories.png)

### Edit Expense
![Edit Expense](https://github.com/jothika-08-joo/Expense-Tracker/blob/d5b7fce45e53c2e303287e70ee0e6cc881d909d7/edit_expense.png)

## 🧑‍💻 Author

**Jothika K**  
B.Sc. Computer Science — Government Arts College (Autonomous), Salem  
- GitHub: [@jothika-08-joo](https://github.com/jothika-08-joo)  
- LinkedIn: [jothika-kumaravadivel](https://linkedin.com/in/jothika-kumaravadivel-591a1a2b2)  
- Email: jothikakumaravadivel@gmail.com
