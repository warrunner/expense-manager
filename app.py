from flask import Flask
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(
    os.path.join(project_dir,"mydatabase.db")
)

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = database_file

db = SQLAlchemy(app) 

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename= db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category=db.Column(db.String(50), nullable=False)

@app.route('/')
def add():
    return redirect('/addview')

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    total = 0
    t_business = 0
    t_other = 0
    t_food = 0
    t_entertainment = 0
    for expense in expenses:
        total += expense.amount
        if(expense.category == 'business'):
            t_business += expense.amount 
        elif expense.category == 'other':
            t_other += expense.amount 
        elif expense.category == 'food':
            t_food += expense.amount
        elif expense.category == 'entertainment':
            t_entertainment += expense.amount
    print(total)
    return render_template(
        'expenses.html', 
        expenses = expenses, 
        total=total, 
        t_business=t_business, 
        t_other = t_other, 
        t_food = t_food, 
        t_entertainment= t_entertainment
    )

@app.route('/addexpense', methods=['POST'])
def addexpense():
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    print(date + " " + expensename + " " + amount + " " + category)
    expense = Expense(date=date, expensename=expensename, amount=amount,category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route('/delete/<int:id>')
def delete(id):
    expense = Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")


@app.route('/updateexpense/<int:id>')
def updateexpense(id):
    expense = Expense.query.filter_by(id=id).first()
    return render_template('updateexpense.html', expense=expense)

@app.route('/edit', methods=['POST'])
def update():
    id = request.form['id']
    date = request.form['date']
    expensename = request.form['expensename']
    amount = request.form['amount']
    category = request.form['category']
    expense = Expense.query.filter_by(id=id).first()
    expense.date = date 
    expense.amount = amount
    expense.category = category 
    expense.expensename = expensename 
    db.session.commit()
    return redirect("/expenses")

@app.route('/addview', methods=['GET', 'POST'])
def addview():
    if request.method == 'GET':
        expenses = Expense.query.all()
        total = 0
        t_business = 0
        t_other = 0
        t_food = 0
        t_entertainment = 0
        for expense in expenses:
            total += expense.amount
            if(expense.category == 'business'):
                t_business += expense.amount 
            elif expense.category == 'other':
                t_other += expense.amount 
            elif expense.category == 'food':
                t_food += expense.amount
            elif expense.category == 'entertainment':
                t_entertainment += expense.amount
        print(total)
    elif request.method == 'POST':
        date = request.form['date']
        expensename = request.form['expensename']
        amount = request.form['amount']
        category = request.form['category']
        print(date + " " + expensename + " " + amount + " " + category)
        expense = Expense(date=date, expensename=expensename, amount=amount,category=category)
        db.session.add(expense)
        db.session.commit()
        return redirect("/addview")

    return render_template(
        'addview.html', 
        expenses = expenses, 
        total=total, 
        t_business=t_business, 
        t_other = t_other, 
        t_food = t_food, 
        t_entertainment= t_entertainment
    )


if __name__ == "__main__":
    app.run(debug=True)