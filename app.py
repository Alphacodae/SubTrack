from flask import Flask, render_template, request, redirect, url_for, flash
from db import fetch_all, execute_query
from datetime import date
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


# ─── DASHBOARD ───────────────────────────────────────────────
@app.route('/')
def dashboard():
    total_subscribers = fetch_all("SELECT COUNT(*) as count FROM User WHERE status='Active'")[0]['count']
    total_revenue = fetch_all("SELECT COALESCE(SUM(amount_paid),0) as total FROM Payment WHERE status='Successful'")[0]['total']
    active_subs = fetch_all("SELECT COUNT(*) as count FROM User_Subscription WHERE status='Active'")[0]['count']
    expiring_soon = fetch_all("SELECT * FROM vw_expiring_soon")
    return render_template('dashboard.html',
        total_subscribers=total_subscribers,
        total_revenue=total_revenue,
        active_subs=active_subs,
        expiring_soon=expiring_soon)

# ─── SUBSCRIBERS ─────────────────────────────────────────────
@app.route('/subscribers')
def subscribers():
    users = fetch_all("SELECT * FROM User ORDER BY created_at DESC")
    return render_template('subscribers.html', users=users)

@app.route('/subscribers/add', methods=['GET', 'POST'])
def add_subscriber():
    if request.method == 'POST':
        execute_query("""
            INSERT INTO User (tenant_id, first_name, last_name, email, phone, password_hash, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Active')
        """, (1, request.form['first_name'], request.form['last_name'],
              request.form['email'], request.form['phone'], request.form['password']))
        flash('Subscriber added successfully!', 'success')
        return redirect(url_for('subscribers'))
    return render_template('add_subscriber.html')

@app.route('/subscribers/delete/<int:user_id>')
def delete_subscriber(user_id):
    execute_query("DELETE FROM User WHERE user_id = %s", (user_id,))
    flash('Subscriber deleted.', 'info')
    return redirect(url_for('subscribers'))

# ─── PLANS ───────────────────────────────────────────────────
@app.route('/plans')
def plans():
    plans = fetch_all("SELECT * FROM Subscription_Plan ORDER BY price ASC")
    return render_template('plans.html', plans=plans)

@app.route('/plans/add', methods=['GET', 'POST'])
def add_plan():
    if request.method == 'POST':
        execute_query("""
            INSERT INTO Subscription_Plan (tenant_id, plan_name, price, billing_cycle)
            VALUES (%s, %s, %s, %s)
        """, (1, request.form['plan_name'], request.form['price'], request.form['billing_cycle']))
        flash('Plan added successfully!', 'success')
        return redirect(url_for('plans'))
    return render_template('add_plan.html')

# ─── PAYMENTS ────────────────────────────────────────────────
@app.route('/payments')
def payments():
    payments = fetch_all("""
        SELECT p.*, i.amount_due, i.due_date, us.user_id
        FROM Payment p
        JOIN Invoice i ON p.invoice_id = i.invoice_id
        JOIN User_Subscription us ON i.subscription_id = us.subscription_id
        ORDER BY p.payment_date DESC
    """)
    return render_template('payments.html', payments=payments)

@app.route('/payments/add', methods=['GET', 'POST'])
def add_payment():
    invoices = fetch_all("SELECT i.*, u.first_name, u.last_name FROM Invoice i JOIN User_Subscription us ON i.subscription_id = us.subscription_id JOIN User u ON us.user_id = u.user_id WHERE i.status='Pending'")
    if request.method == 'POST':
        execute_query("""
            INSERT INTO Payment (invoice_id, amount_paid, payment_date, payment_method, status)
            VALUES (%s, %s, %s, %s, 'Successful')
        """, (request.form['invoice_id'], request.form['amount_paid'],
              date.today(), request.form['payment_method']))
        execute_query("UPDATE Invoice SET status='Paid' WHERE invoice_id=%s", (request.form['invoice_id'],))
        flash('Payment recorded successfully!', 'success')
        return redirect(url_for('payments'))
    return render_template('add_payment.html', invoices=invoices)

# ─── SUBSCRIPTIONS ───────────────────────────────────────────
@app.route('/subscriptions')
def subscriptions():
    subs = fetch_all("""
        SELECT us.*, u.first_name, u.last_name, sp.plan_name, sp.price
        FROM User_Subscription us
        JOIN User u ON us.user_id = u.user_id
        JOIN Subscription_Plan sp ON us.plan_id = sp.plan_id
        ORDER BY us.end_date ASC
    """)
    return render_template('subscriptions.html', subs=subs)

@app.route('/subscriptions/add', methods=['GET', 'POST'])
def add_subscription():
    users = fetch_all("SELECT user_id, first_name, last_name FROM User WHERE status='Active'")
    plans = fetch_all("SELECT plan_id, plan_name, price FROM Subscription_Plan WHERE is_active=1")
    if request.method == 'POST':
        execute_query("""
            INSERT INTO User_Subscription (user_id, plan_id, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, 'Active')
        """, (request.form['user_id'], request.form['plan_id'],
              request.form['start_date'], request.form['end_date']))
        flash('Subscription added successfully!', 'success')
        return redirect(url_for('subscriptions'))
    return render_template('add_subscription.html', users=users, plans=plans)

# ─── RUN ─────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False') == 'True')