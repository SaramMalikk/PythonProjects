from customer_file import *
from rental_file import *
from branches_file import *
from car_file import *
from payment_file import *
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/create_customer', methods=['POST'])
def create_customers():
    data = request.get_json()
    db = Customers()
    response, status_code = db.create(data)
    return jsonify(response), status_code


@app.route('/view_customer', methods=['GET', 'POST'])
def view_customer():
    data = request.get_json()
    db = Customers()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route('/remove_customer', methods=['POST'])
def remove_customer():
    data = request.get_json()
    db = Customers()
    response, status_code = db.remove(data)
    return jsonify(response), status_code


@app.route('/edit_customer', methods=['POST'])
def edit_customer():
    data = request.get_json()
    db = Customers()
    response, status_code = db.edit(data)
    return jsonify(response), status_code


@app.route('/create_car_rents', methods=['POST'])
def create_car_rents():
    data = request.get_json()
    db = Cars()
    response, status_code = db.create_rent(data)
    return jsonify(response), status_code


@app.route('/enter_car', methods=['POST'])
def enter_car():
    data = request.get_json()
    db = Cars()
    response, status_code = db.create(data)
    return jsonify(response), status_code


@app.route('/view_cars', methods=['GET'])
def view_cars():
    data = request.get_json()
    db = Cars()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route('/view_all_cars', methods=['GET'])
def view_all_cars():
    db = Cars()
    response, status_code = db.view_all()
    return jsonify(response), status_code


@app.route('/remove_cars', methods=['POST', 'GET'])
def remove_cars():
    data = request.get_json()
    db = Cars()
    response, status_code = db.remove(data)
    return jsonify(response), status_code


@app.route('/edit_cars', methods=['POST', 'GET'])
def edit_cars():
    data = request.get_json()
    db = Cars()
    response, status_code = db.edit(data)
    return jsonify(response), status_code


@app.route('/car_booking', methods=['POST'])
def car_booking():
    data = request.get_json()
    db = Rentals()
    response, status_code = db.booking(data)
    return jsonify(response), status_code


@app.route('/check_availability', methods=['GET'])
def check_availability():
    data = request.get_json()
    db = Rentals()
    response, status_code = db.availability(data)
    return jsonify(response), status_code


@app.route('/update_booking', methods=['POST'])
def update_booking():
    data = request.get_json()
    db = Rentals()
    response, status_code = db.edit(data)
    return jsonify(response), status_code


@app.route('/cancel_booking', methods=['POST'])
def cancel_booking():
    data = request.get_json()
    db = Rentals()
    response, status_code = db.cancel(data)
    return jsonify(response), status_code


@app.route('/view_booking', methods=['POST', 'GET'])
def view_booking():
    data = request.get_json()
    db = Rentals()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route('/enter_payments', methods=['POST'])
def enter_payments():
    data = request.get_json()
    db = Payments()
    response, status_code = db.payments(data)
    return jsonify(response), status_code


@app.route('/view_payments', methods=['POST', 'GET'])
def view_payments():
    data = request.get_json()
    db = Payments()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route('/create_branch', methods=['POST'])
def create_branch():
    data = request.get_json()
    db = Branches()
    response, status_code = db.create(data)
    return jsonify(response), status_code


@app.route('/view_branches', methods=['GET'])
def view_branches():
    db = Branches()
    response, status_code = db.view()
    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(debug=True)
