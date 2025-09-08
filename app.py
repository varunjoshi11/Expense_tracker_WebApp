from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests, useful for local dev/testing

# In-memory storage for simplicity - replace with DB as needed
expenses = []

# Helper to find expense by id
def find_expense(expense_id):
    return next((e for e in expenses if e['id'] == expense_id), None)

@app.route('/expenses', methods=['GET'])
def get_expenses():
    # Return all expenses sorted by timestamp descending
    sorted_expenses = sorted(expenses, key=lambda e: e['timestamp'], reverse=True)
    return jsonify(sorted_expenses)

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    required = ['description', 'amount', 'category', 'date']
    if not all(key in data for key in required):
        return jsonify({"error": "Missing fields"}), 400

    try:
        amount = float(data['amount'])
        datetime.datetime.strptime(data['date'], '%Y-%m-%d')  # validate date
    except Exception:
        return jsonify({"error": "Invalid amount or date format"}), 400

    expense = {
        'id': int(datetime.datetime.now().timestamp() * 1000),  # simple unique id
        'description': data['description'],
        'amount': amount,
        'category': data['category'],
        'date': data['date'],
        'timestamp': datetime.datetime.now().isoformat()
    }
    expenses.append(expense)
    return jsonify(expense), 201

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = find_expense(expense_id)
    if not expense:
        return jsonify({"error": "Expense not found"}), 404
    expenses.remove(expense)
    return jsonify({"message": "Deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
