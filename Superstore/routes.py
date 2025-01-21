from categories_file import *
from products_file import *
from supplier_file import *
from inventory_file import *
from order_file import *
from sell_file import *
from employee_file import *
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS


CORS(app)  # Enable CORS for the whole app


@app.route("/enter_categories", methods=["POST"])
def enter_categories():
    data = request.get_json()
    db = Categories()
    response, status_code = db.category_info(data)
    return jsonify(response), status_code


@app.route("/view_categories", methods=["GET", "POST"])
def view_categories():
    db = Categories()
    response, status_code = db.view()
    return jsonify(response), status_code


@app.route("/enter_products", methods=["POST"])
def enter_products():
    data = request.get_json()
    db = Products()
    response, status_code = db.products_data(data)
    return jsonify(response), status_code


@app.route("/view_products", methods=["GET" ,"POST"])
def view_products():
    data = request.get_json()
    db = Products()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route("/view_all_products", methods=["GET", 'POST'])
def view_all_products():
    db = Products()
    response, status_code = db.view_all()
    return jsonify(response), status_code


@app.route("/enter_suppliers", methods=["POST"])
def enter_suppliers():
    data = request.get_json()
    db = Supplier()
    response, status_code = db.suppliers_data(data)
    return jsonify(response), status_code


@app.route("/view_suppliers", methods=["GET"])
def view_suppliers():
    db = Supplier()
    response, status_code = db.view()
    return jsonify(response), status_code


@app.route("/remove_suppliers", methods=["POST"])
def remove_suppliers():
    data = request.get_json()
    db = Supplier()
    response, status_code = db.remove(data)
    return jsonify(response), status_code


# @app.route("/update_inventory", methods=["POST"])
# def update_inventory():
#     data = request.get_json()
#     db = Inventory()
#     response, status_code = db.inventory_info(data)
#     return jsonify(response), status_code


@app.route("/view_inventory", methods=["GET", "POST"])
def view_inventory():
    data = request.get_json()
    db = Inventory()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route("/update_order", methods=["POST"])
def update_order():
    data = request.get_json()
    db = Orders()
    response, status_code = db.enter_order(data)
    return jsonify(response), status_code


@app.route("/view_order", methods=["GET", "POST"])
def view_order():
    data = request.get_json()
    db = Orders()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route("/enter_sell", methods=["POST"])
def enter_sell():
    data = request.get_json()
    db = Sell()
    response, status_code = db.sell_data(data)
    return jsonify(response), status_code


@app.route("/view_sell_by_date", methods=["POST", 'GET'])
def view_sell_by_date():
    data = request.get_json()
    db = Sell()
    response, status_code = db.view_by_date(data)
    return jsonify(response), status_code


@app.route("/view_sell", methods=["GET", "POST"])
def view_sell():
    data = request.get_json()
    db = Sell()
    response, status_code = db.view(data)
    return jsonify(response), status_code


@app.route("/enter_employee", methods=["POST"])
def enter_employee():
    data = request.get_json()
    db = Employee()
    response, status_code = db.employee_data(data)
    return jsonify(response), status_code


@app.route("/view_employee", methods=["GET"])
def view_employee():
    db = Employee()
    response, status_code = db.view()
    return jsonify(response), status_code


@app.route("/remove_employee", methods=["POST"])
def remove_employee():
    data = request.get_json()
    db = Employee()
    response, status_code = db.remove(data)
    return jsonify(response), status_code


if __name__ == '__main__':
    app.run(debug=True)
