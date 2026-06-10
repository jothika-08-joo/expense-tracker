from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db,  User, Expense, Category


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(username = username).first():
            flash('username already exist', 'error')
        else:
            new_user = User(username = username, password = password)
            db.session.add(new_user) 
            db.session.commit()

            flash('registeration successful. please login', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')     


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username = request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('invalid username or password!', 'error')
    return render_template('login.html')  


@app.route('/dashboard')
@login_required
def dashboard():
    expenses = Expense.query.filter_by(user_id = current_user.id).all()

    total_expenses = sum(exp.amount for exp in expenses)   

    current_month = datetime.now().strftime('%Y-%m')
    monthly_total = sum(
        exp.amount for exp in expenses 
        if exp.date.startswith(current_month)
    )

    category_totals = {}
    for exp in expenses:
        cat_name = exp.category.name if exp.category else "uncategorized"
        category_totals[cat_name] = category_totals.get(cat_name, 0) + exp.amount


    return render_template(
        'dashboard.html',
        total_expenses = total_expenses,
        username = current_user.username,
        expenses = expenses,
        monthly_total = monthly_total,
        category_totals = category_totals
    )     


@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add_expense():
    categories = Category.query.all()

    if request.method == 'POST':
        try:

            title = request.form['title']
            amount = float(request.form['amount'])
            date = request.form['date']
            category_id = request.form['category_id']

            new_expense = Expense(
                title = title,
                amount = amount,
                date = date,
                user_id = current_user.id,
                category_id = category_id
            )

            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')    

    return render_template('add_expense.html', categories = categories)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    expense = Expense.query.get_or_404(id)
    categories = Category.query.all()

    if expense.user_id != current_user.id:
        flash('unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        try:

            expense.title = request.form['title']
            expense.amount = float(request.form['amount'])
            expense.date = request.form['date']
            expense.category_id = request.form['category_id'] 

            db.session.commit()   
            flash('expense updated!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
    return render_template('edit_expense.html', expense = expense, categories = categories) 


@app.route('/delete/<int:id>')
@login_required
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    if expense.user_id != current_user.id:
        flash('unauthorized access!', 'error')
        return redirect(url_for('dashboard'))
    try:

        db.session.delete(expense)
        db.session.commit()
        flash('expense deleted!', 'success')
    except Exception as e:
        flash(f'Error deleting expense: {str(e)}', 'error')

    return redirect(url_for('dashboard'))  

@app.route('/logout')
@login_required   
def logout():
    logout_user()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

#categories CRUD
@app.route('/categories')   
@login_required
def list_categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods = ['GET','POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        if Category.query.filter_by(name=name).first():
            flash("category already exists!", 'error')
        else:
            try:

                new_cat = Category(name=name, description=description)
                db.session.add(new_cat)
                db.session.commit()
                flash('category added!', 'success')
                return redirect(url_for('list_categories'))
            except Exception as e:
                flash(f'Error adding category: {str(e)}', 'error')

    return render_template('add_category.html') 
   
 


@app.route('/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        try:

            category.name = request.form['name']
            category.description = request.form('description', '')
            db.session.commit()
            flash('category updated successfully', ' success')
            return redirect(url_for('list_categories'))
        except Exception as e:
            flash(f'Error updating category: {str(e)}', 'error')
    
    return render_template('edit_category.html', category=category)    


@app.route('/categories/delete/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    try:
        
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting category: {str(e)}', 'error')    
    return redirect(url_for('list_categories'))



    



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)    